"""Multi-step booking conversation.

Flow:
    1. User taps "Book Appointment".
    2. Bot asks for the user's full name.
    3. Bot asks for the user's phone number (validated).
    4. Bot saves/logs the lead, confirms to the user, and optionally
       notifies an admin chat.

Send /cancel at any point to abort the flow.
"""
import logging
import re

from aiogram import Bot, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from config import ADMIN_CHAT_ID, BUSINESS_NAME
from keyboards import CB, back_to_menu_keyboard
from storage import save_lead

logger = logging.getLogger(__name__)

router = Router()

PHONE_RE = re.compile(r"^\+?[0-9()\-\s]{7,20}$")


class Booking(StatesGroup):
    name = State()
    phone = State()


@router.callback_query(F.data == CB.BOOK)
async def start_booking(callback: CallbackQuery, state: FSMContext) -> None:
    """Entry point: user tapped 'Book Appointment'."""
    await callback.answer()
    await state.set_state(Booking.name)
    await callback.message.edit_text(
        "📅 *Book an Appointment*\n\n"
        "Let's get a few details so our team can reach out to confirm a time.\n\n"
        "First, what's your *full name*?\n\n"
        "_(Send /cancel at any time to stop.)_",
        parse_mode=ParseMode.MARKDOWN,
    )


@router.message(Booking.name, F.text, ~F.text.startswith("/"))
async def receive_name(message: Message, state: FSMContext) -> None:
    """Store the provided name and ask for a phone number."""
    name = (message.text or "").strip()

    if len(name) < 2:
        await message.answer(
            "That doesn't look like a valid name. Please enter your full name:"
        )
        return

    await state.update_data(lead_name=name)
    await state.set_state(Booking.phone)
    await message.answer(
        f"Thanks, {name}! 📱 Now, what's the best *phone number* to reach you?\n\n"
        "_(e.g. +1 555 123 4567)_",
        parse_mode=ParseMode.MARKDOWN,
    )


@router.message(Booking.phone, F.text, ~F.text.startswith("/"))
async def receive_phone(message: Message, state: FSMContext, bot: Bot) -> None:
    """Validate the phone number, save the lead, and confirm to the user."""
    phone = (message.text or "").strip()

    if not PHONE_RE.match(phone):
        await message.answer(
            "That doesn't look like a valid phone number. Please try again "
            "(e.g. +1 555 123 4567):"
        )
        return

    data = await state.get_data()
    name = data.get("lead_name", "Unknown")
    user = message.from_user
    await state.clear()

    save_lead(
        user_id=user.id,
        username=user.username or "",
        full_name=user.full_name or "",
        name=name,
        phone=phone,
    )

    await message.answer(
        "✅ *You're all set!*\n\n"
        f"Thanks, {name} — a member of the {BUSINESS_NAME} team will contact you "
        f"at {phone} shortly to confirm your appointment.",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_to_menu_keyboard(),
    )

    if ADMIN_CHAT_ID:
        try:
            await bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=(
                    "🆕 New lead!\n"
                    f"Name: {name}\n"
                    f"Phone: {phone}\n"
                    f"Telegram: @{user.username or 'N/A'} (id {user.id})"
                ),
            )
        except Exception:
            logger.exception("Failed to notify admin chat about the new lead.")


@router.message(StateFilter(Booking.name, Booking.phone), Command("cancel"))
async def cancel_booking(message: Message, state: FSMContext) -> None:
    """Handle /cancel — abort the booking conversation."""
    await state.clear()
    await message.answer(
        "Booking cancelled. Send /start to open the menu again.",
        reply_markup=ReplyKeyboardRemove(),
    )

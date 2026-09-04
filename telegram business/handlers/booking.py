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

from config import ADMIN_CHAT_ID
from i18n import get_lang, t
from keyboards import CB, back_to_menu_keyboard
from storage import save_lead

logger = logging.getLogger(__name__)

router = Router()

PHONE_RE = re.compile(r"^\+?[0-9()\-\s]{7,20}$")


class Booking(StatesGroup):
    name = State()
    phone = State()


def _lang(event: Message | CallbackQuery) -> str:
    return get_lang(event.from_user.id if event.from_user else None)


@router.callback_query(F.data == CB.BOOK)
async def start_booking(callback: CallbackQuery, state: FSMContext) -> None:
    """Entry point: user tapped 'Book Appointment'."""
    await callback.answer()
    lang = _lang(callback)
    await state.set_state(Booking.name)
    await callback.message.edit_text(
        t(lang, "booking_intro"),
        parse_mode=ParseMode.MARKDOWN,
    )


@router.message(Booking.name, F.text, ~F.text.startswith("/"))
async def receive_name(message: Message, state: FSMContext) -> None:
    """Store the provided name and ask for a phone number."""
    lang = _lang(message)
    name = (message.text or "").strip()

    if len(name) < 2:
        await message.answer(t(lang, "booking_bad_name"))
        return

    await state.update_data(lead_name=name)
    await state.set_state(Booking.phone)
    await message.answer(
        t(lang, "booking_ask_phone", name=name),
        parse_mode=ParseMode.MARKDOWN,
    )


@router.message(Booking.phone, F.text, ~F.text.startswith("/"))
async def receive_phone(message: Message, state: FSMContext, bot: Bot) -> None:
    """Validate the phone number, save the lead, and confirm to the user."""
    lang = _lang(message)
    phone = (message.text or "").strip()

    if not PHONE_RE.match(phone):
        await message.answer(t(lang, "booking_bad_phone"))
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
        task="appointment booking",
    )

    await message.answer(
        t(lang, "booking_done", name=name, phone=phone),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_to_menu_keyboard(lang),
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
    lang = _lang(message)
    await state.clear()
    await message.answer(
        t(lang, "booking_cancel"),
        reply_markup=ReplyKeyboardRemove(),
    )

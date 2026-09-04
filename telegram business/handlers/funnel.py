"""Order funnel: niche → task → contact."""
import logging
import re

from aiogram import Bot, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from config import ADMIN_CHAT_ID
from i18n import get_lang, t
from keyboards import CB, main_menu_keyboard
from storage import save_lead

logger = logging.getLogger(__name__)

router = Router()

CONTACT_RE = re.compile(r"^(@[\w\d_]{3,}|[\d+\-\s()]{7,20})$", re.IGNORECASE)


class Order(StatesGroup):
    niche = State()
    task = State()
    contact = State()


def _lang(event: Message | CallbackQuery) -> str:
    return get_lang(event.from_user.id if event.from_user else None)


@router.callback_query(F.data == CB.ORDER)
async def start_order(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    lang = _lang(callback)
    await state.set_state(Order.niche)
    await callback.message.edit_text(
        t(lang, "ask_niche"),
        parse_mode=ParseMode.MARKDOWN,
    )


@router.message(Order.niche, F.text, ~F.text.startswith("/"))
async def receive_niche(message: Message, state: FSMContext) -> None:
    lang = _lang(message)
    niche = (message.text or "").strip()
    if len(niche) < 2:
        await message.answer(t(lang, "need_niche"))
        return
    await state.update_data(niche=niche)
    await state.set_state(Order.task)
    await message.answer(
        t(lang, "ask_task", niche=niche),
        parse_mode=ParseMode.MARKDOWN,
    )


@router.message(Order.task, F.text, ~F.text.startswith("/"))
async def receive_task(message: Message, state: FSMContext) -> None:
    lang = _lang(message)
    task = (message.text or "").strip()
    if len(task) < 3:
        await message.answer(t(lang, "need_task"))
        return
    await state.update_data(task=task)
    await state.set_state(Order.contact)
    await message.answer(
        t(lang, "ask_contact"),
        parse_mode=ParseMode.MARKDOWN,
    )


@router.message(Order.contact, F.text, ~F.text.startswith("/"))
async def receive_contact(message: Message, state: FSMContext, bot: Bot) -> None:
    lang = _lang(message)
    contact = (message.text or "").strip()
    if not CONTACT_RE.match(contact):
        await message.answer(t(lang, "need_contact"))
        return

    data = await state.get_data()
    niche = data.get("niche", "")
    task = data.get("task", "")
    user = message.from_user
    await state.clear()

    save_lead(
        user_id=user.id if user else 0,
        username=(user.username if user else "") or "",
        full_name=(user.full_name if user else "") or "",
        niche=niche,
        task=task,
        contact=contact,
    )

    await message.answer(
        t(lang, "thanks", niche=niche, task=task, contact=contact),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard(lang),
    )

    if ADMIN_CHAT_ID:
        try:
            await bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=(
                    "🆕 New bot project inquiry\n"
                    f"Niche: {niche}\n"
                    f"Task: {task}\n"
                    f"Contact: {contact}\n"
                    f"Telegram: @{user.username if user and user.username else 'N/A'} "
                    f"(id {user.id if user else 'N/A'})"
                ),
            )
        except Exception:
            logger.exception("Failed to notify admin about inquiry.")


@router.message(StateFilter(Order.niche, Order.task, Order.contact), Command("cancel"))
async def cancel_order(message: Message, state: FSMContext) -> None:
    lang = _lang(message)
    await state.clear()
    await message.answer(
        t(lang, "cancelled"),
        reply_markup=main_menu_keyboard(lang),
    )

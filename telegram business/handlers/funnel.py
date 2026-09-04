"""Lead-generation funnel (conversion-focused).

Flow:
    1. /start — language (once), then welcome + category buttons.
    2. Category → describe problem (text or photo).
    3. Phone number → save lead and thank the user.
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
from i18n import CHOOSE_LANGUAGE, get_lang, set_lang, t
from keyboards import (
    CB,
    category_keyboard,
    home_keyboard,
    language_keyboard,
    nav_button_texts,
    nav_keyboard,
    welcome_funnel_keyboard,
)
from storage import save_lead

logger = logging.getLogger(__name__)

router = Router()

PHONE_RE = re.compile(r"^\+?[0-9()\-\s]{7,20}$")


class Funnel(StatesGroup):
    category = State()
    task = State()
    waiting_for_contact = State()


CATEGORY_CALLBACKS = {
    CB.CAT_REPAIR: "cat_repair",
    CB.CAT_CLEANING: "cat_cleaning",
    CB.CAT_OTHER: "cat_other",
    # Older buttons still map into the simplified set.
    CB.CAT_PLUMBING: "cat_repair",
    CB.CAT_ELECTRICAL: "cat_repair",
    CB.CAT_HANDYMAN: "cat_repair",
    CB.CAT_GARDEN: "cat_other",
}


def _uid(event: Message | CallbackQuery) -> int | None:
    return event.from_user.id if event.from_user else None


def _lang(event: Message | CallbackQuery) -> str:
    return get_lang(_uid(event))


async def finish_funnel(
    message: Message,
    state: FSMContext,
    bot: Bot,
    *,
    phone: str,
) -> None:
    """Save the lead and send the thank-you + menu."""
    lang = _lang(message)
    user = message.from_user
    data = await state.get_data()
    task = data.get("task", "")
    category = data.get("category", "")
    photo_file_id = data.get("photo_file_id", "")
    name = (user.full_name if user else "") or "Unknown"
    await state.clear()

    save_lead(
        user_id=user.id if user else 0,
        username=(user.username if user else "") or "",
        full_name=(user.full_name if user else "") or "",
        name=name,
        phone=phone,
        task=task,
        category=category,
        photo_file_id=photo_file_id,
    )

    first = name.split()[0] if name else ("there" if lang == "en" else "Tam")
    await message.answer(
        f"{t(lang, 'funnel_thanks', name=first)}\n\n{t(lang, 'funnel_menu_after')}",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=nav_keyboard(lang),
    )
    await state.set_state(Funnel.category)
    await message.answer(
        t(lang, "funnel_ask_category"),
        reply_markup=welcome_funnel_keyboard(lang),
    )

    if ADMIN_CHAT_ID:
        try:
            await bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=(
                    "🆕 New funnel lead!\n"
                    f"Name: {name}\n"
                    f"Phone: {phone}\n"
                    f"Category: {category}\n"
                    f"Task: {task}\n"
                    f"Photo: {'yes' if photo_file_id else 'no'}\n"
                    f"Telegram: @{user.username if user and user.username else 'N/A'} "
                    f"(id {user.id if user else 'N/A'})"
                ),
            )
        except Exception:
            logger.exception("Failed to notify admin chat about the new lead.")


@router.callback_query(F.data.in_({CB.LANG_EN, CB.LANG_PL}))
async def choose_language(callback: CallbackQuery, state: FSMContext) -> None:
    """Save language, then show the conversion welcome with categories."""
    lang = "en" if callback.data == CB.LANG_EN else "pl"
    if callback.from_user:
        set_lang(callback.from_user.id, lang)

    data = await state.get_data()
    dest = data.get("after_lang", "home")
    await callback.answer()

    await state.set_state(Funnel.category)

    if dest == "category":
        await callback.message.edit_text(
            t(lang, "funnel_ask_category"),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=category_keyboard(lang),
        )
        await callback.message.answer(
            t(lang, "commands_hint"),
            reply_markup=nav_keyboard(lang),
        )
        return

    from handlers.commands import home_text

    await callback.message.edit_text(
        home_text(lang),
        parse_mode=ParseMode.MARKDOWN,
    )
    await callback.message.answer(
        t(lang, "funnel_ask_category"),
        reply_markup=welcome_funnel_keyboard(lang),
    )
    await callback.message.answer(
        t(lang, "commands_hint"),
        reply_markup=nav_keyboard(lang),
    )


@router.callback_query(F.data == CB.CHANGE_LANG)
async def change_language(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.update_data(after_lang="home")
    await callback.message.edit_text(CHOOSE_LANGUAGE, reply_markup=language_keyboard())


@router.callback_query(F.data == CB.NEW_REQUEST)
async def start_new_request(callback: CallbackQuery, state: FSMContext) -> None:
    """Show category picker (same as welcome conversion screen)."""
    await callback.answer()
    lang = _lang(callback)
    await state.set_state(Funnel.category)
    await callback.message.edit_text(
        t(lang, "funnel_ask_category"),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=category_keyboard(lang),
    )


@router.callback_query(F.data.in_(set(CATEGORY_CALLBACKS)))
async def receive_category(callback: CallbackQuery, state: FSMContext) -> None:
    """Category chosen → ask for text description or photo."""
    await callback.answer()
    lang = _lang(callback)
    cat_key = CATEGORY_CALLBACKS[callback.data]
    category = t(lang, cat_key)
    await state.update_data(category=category, category_key=cat_key)
    await state.set_state(Funnel.task)
    await callback.message.edit_text(
        t(lang, "funnel_ask_task", category=category),
        parse_mode=ParseMode.MARKDOWN,
    )


async def _ask_for_phone(message: Message, state: FSMContext, lang: str) -> None:
    await state.set_state(Funnel.waiting_for_contact)
    await message.answer(
        t(lang, "funnel_ask_contact"),
        parse_mode=ParseMode.MARKDOWN,
    )


@router.message(Funnel.task, F.photo)
async def receive_task_photo(message: Message, state: FSMContext) -> None:
    """Accept a photo, thank the user, then ask for a phone number."""
    lang = _lang(message)
    photo = message.photo[-1]
    caption = (message.caption or "").strip()
    data = await state.get_data()
    category = data.get("category", "")
    task = caption or t(lang, "funnel_photo_received")
    if category:
        task = f"[{category}] {task}"

    await state.update_data(task=task, photo_file_id=photo.file_id)
    await message.answer(t(lang, "funnel_photo_received"))
    await _ask_for_phone(message, state, lang)


@router.message(Funnel.task, F.text, ~F.text.startswith("/"))
async def receive_task(message: Message, state: FSMContext) -> None:
    """Store the text description and ask for a phone number."""
    lang = _lang(message)
    task = (message.text or "").strip()
    if task in nav_button_texts():
        return
    if len(task) < 3:
        await message.answer(t(lang, "funnel_need_task"))
        return

    data = await state.get_data()
    category = data.get("category", "")
    if category:
        task = f"[{category}] {task}"

    await state.update_data(task=task)
    await _ask_for_phone(message, state, lang)


@router.message(Funnel.waiting_for_contact, F.contact)
async def receive_shared_contact(message: Message, state: FSMContext, bot: Bot) -> None:
    phone = (message.contact.phone_number or "").strip()
    if not PHONE_RE.match(phone):
        lang = _lang(message)
        await message.answer(t(lang, "funnel_need_contact"))
        return
    await finish_funnel(message, state, bot, phone=phone)


@router.message(Funnel.waiting_for_contact, F.text, ~F.text.startswith("/"))
async def receive_phone_text(message: Message, state: FSMContext, bot: Bot) -> None:
    lang = _lang(message)
    phone = (message.text or "").strip()
    if phone in nav_button_texts():
        return
    if not PHONE_RE.match(phone):
        await message.answer(t(lang, "funnel_need_contact"))
        return
    await finish_funnel(message, state, bot, phone=phone)


@router.message(StateFilter(Funnel.category, Funnel.task, Funnel.waiting_for_contact), Command("cancel"))
async def cancel_funnel(message: Message, state: FSMContext) -> None:
    lang = _lang(message)
    await state.clear()
    await message.answer(
        t(lang, "funnel_cancel"),
        reply_markup=nav_keyboard(lang),
    )

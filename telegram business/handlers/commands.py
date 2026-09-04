"""/start, /help and language selection."""
from aiogram import Bot, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand, CallbackQuery, Message

from i18n import CHOOSE_LANGUAGE, get_lang, has_lang, set_lang, t
from keyboards import CB, language_keyboard, main_menu_keyboard

router = Router()

_LANG_BY_CB = {
    CB.LANG_EN: "en",
    CB.LANG_PL: "pl",
    CB.LANG_RU: "ru",
    CB.LANG_UK: "uk",
}


async def send_main_menu(message: Message, lang: str) -> None:
    await message.answer(
        t(lang, "welcome"),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard(lang),
    )


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    user_id = message.from_user.id if message.from_user else None
    if not has_lang(user_id):
        await message.answer(CHOOSE_LANGUAGE, reply_markup=language_keyboard())
        return
    await send_main_menu(message, get_lang(user_id))


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    lang = get_lang(message.from_user.id if message.from_user else None)
    await message.answer(t(lang, "help"))


@router.callback_query(F.data.in_(set(_LANG_BY_CB)))
async def choose_language(callback: CallbackQuery, state: FSMContext) -> None:
    lang = _LANG_BY_CB[callback.data]
    if callback.from_user:
        set_lang(callback.from_user.id, lang)
    await callback.answer()
    await state.clear()
    await callback.message.edit_text(
        t(lang, "welcome"),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard(lang),
    )


@router.callback_query(F.data == CB.CHANGE_LANG)
async def change_language(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.edit_text(CHOOSE_LANGUAGE, reply_markup=language_keyboard())


@router.callback_query(F.data == CB.MAIN_MENU)
async def show_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.clear()
    lang = get_lang(callback.from_user.id if callback.from_user else None)
    await callback.message.edit_text(
        t(lang, "welcome"),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard(lang),
    )


async def setup_bot_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Open menu / Меню"),
            BotCommand(command="help", description="Help / Pomoc"),
            BotCommand(command="cancel", description="Cancel / Anuluj"),
        ]
    )

"""Small command section: /start, /new, /help + bottom reply buttons."""
from aiogram import Bot, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand, Message

from i18n import CHOOSE_LANGUAGE, get_lang, has_lang, t
from keyboards import (
    category_keyboard,
    language_keyboard,
    nav_keyboard,
    welcome_funnel_keyboard,
)

router = Router()


def home_text(lang: str) -> str:
    return f"{t(lang, 'menu_welcome')}\n\n{t(lang, 'commands_hint')}"


async def send_home(message: Message, state: FSMContext) -> None:
    """Welcome + category buttons right away (conversion screen)."""
    from handlers.funnel import Funnel

    await state.clear()
    user_id = message.from_user.id if message.from_user else None

    if not has_lang(user_id):
        await state.update_data(after_lang="home")
        await message.answer(CHOOSE_LANGUAGE, reply_markup=language_keyboard())
        return

    lang = get_lang(user_id)
    await state.set_state(Funnel.category)
    await message.answer(
        home_text(lang),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=nav_keyboard(lang),
    )
    await message.answer(
        t(lang, "funnel_ask_category"),
        reply_markup=welcome_funnel_keyboard(lang),
    )


async def start_new_request_flow(message: Message, state: FSMContext) -> None:
    from handlers.funnel import Funnel

    user_id = message.from_user.id if message.from_user else None
    await state.clear()

    if not has_lang(user_id):
        await state.update_data(after_lang="category")
        await message.answer(CHOOSE_LANGUAGE, reply_markup=language_keyboard())
        return

    lang = get_lang(user_id)
    await state.set_state(Funnel.category)
    await message.answer(
        t(lang, "funnel_ask_category"),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=category_keyboard(lang),
    )


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await send_home(message, state)


@router.message(Command("new"))
async def cmd_new(message: Message, state: FSMContext) -> None:
    await start_new_request_flow(message, state)


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    lang = get_lang(message.from_user.id if message.from_user else None)
    await message.answer(
        f"{t(lang, 'help')}\n\n{t(lang, 'commands_hint')}",
        reply_markup=nav_keyboard(lang),
    )


@router.message(F.text.in_({t("en", "btn_nav_menu"), t("pl", "btn_nav_menu")}))
async def btn_menu(message: Message, state: FSMContext) -> None:
    await send_home(message, state)


@router.message(F.text.in_({t("en", "btn_nav_new"), t("pl", "btn_nav_new")}))
async def btn_new(message: Message, state: FSMContext) -> None:
    await start_new_request_flow(message, state)


@router.message(F.text.in_({t("en", "btn_nav_help"), t("pl", "btn_nav_help")}))
async def btn_help(message: Message) -> None:
    await cmd_help(message)


async def setup_bot_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Open the menu"),
            BotCommand(command="new", description="New request"),
            BotCommand(command="help", description="How it works"),
            BotCommand(command="cancel", description="Stop"),
        ],
        language_code="en",
    )
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Otwórz menu"),
            BotCommand(command="new", description="Nowe zgłoszenie"),
            BotCommand(command="help", description="Jak to działa"),
            BotCommand(command="cancel", description="Przerwij"),
        ],
        language_code="pl",
    )
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Menu / Start"),
            BotCommand(command="new", description="New request"),
            BotCommand(command="help", description="Help"),
            BotCommand(command="cancel", description="Cancel"),
        ],
    )

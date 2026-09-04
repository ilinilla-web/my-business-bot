"""/start, /help, and 'Back to Menu' navigation."""
from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from config import BUSINESS_NAME
from keyboards import CB, main_menu_keyboard
from mock_data import WELCOME_TEMPLATE

router = Router()


def _welcome_text() -> str:
    return WELCOME_TEMPLATE.format(business_name=BUSINESS_NAME)


@router.message(CommandStart())
async def start(message: Message) -> None:
    """Handle /start — send the welcome message with the main menu."""
    await message.answer(
        _welcome_text(),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard(),
    )


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    """Handle /help."""
    await message.answer(
        "Use /start to open the main menu at any time.\n"
        "During booking, send /cancel to stop the process."
    )


@router.callback_query(F.data == CB.MAIN_MENU)
async def show_main_menu(callback: CallbackQuery) -> None:
    """Callback handler for the 'Back to Menu' inline button."""
    await callback.answer()
    await callback.message.edit_text(
        _welcome_text(),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu_keyboard(),
    )

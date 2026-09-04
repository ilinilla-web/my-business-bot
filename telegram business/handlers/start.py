"""Home navigation (Back button)."""
from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.commands import home_text
from i18n import get_lang, t
from keyboards import CB, nav_keyboard, welcome_funnel_keyboard

router = Router()


@router.callback_query(F.data == CB.MAIN_MENU)
async def show_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    """Return to welcome + category conversion screen."""
    from handlers.funnel import Funnel

    await callback.answer()
    await state.clear()
    await state.set_state(Funnel.category)
    lang = get_lang(callback.from_user.id if callback.from_user else None)
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

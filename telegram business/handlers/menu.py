"""Info screens: cases, pricing, contact."""
from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from i18n import get_lang, t
from keyboards import CB, back_to_menu_keyboard

router = Router()

_INFO = {
    CB.CASES: "cases",
    CB.PRICING: "pricing",
    CB.CONTACT: "contact_me",
}


@router.callback_query(F.data.in_(set(_INFO)))
async def show_info(callback: CallbackQuery) -> None:
    await callback.answer()
    lang = get_lang(callback.from_user.id if callback.from_user else None)
    key = _INFO[callback.data]
    await callback.message.edit_text(
        t(lang, key),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_to_menu_keyboard(lang),
    )

"""Handlers for info buttons: Services, Pricing, Contact, Reviews."""
import logging

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from i18n import get_lang, t
from keyboards import CB, back_to_menu_keyboard

logger = logging.getLogger(__name__)

router = Router()

_CONTENT_KEY_BY_CALLBACK = {
    CB.SERVICES: "services",
    CB.PRICING: "pricing",
    CB.CONTACT: "contact",
    CB.REVIEWS: "reviews",
}


@router.callback_query(F.data.in_({CB.SERVICES, CB.PRICING, CB.CONTACT, CB.REVIEWS}))
async def show_info(callback: CallbackQuery) -> None:
    """Show info. Reviews also offer 'Send a request' to keep conversion going."""
    await callback.answer()
    lang = get_lang(callback.from_user.id if callback.from_user else None)

    key = _CONTENT_KEY_BY_CALLBACK.get(callback.data)
    if key is None:
        logger.warning("Unhandled menu callback data: %s", callback.data)
        return

    await callback.message.edit_text(
        t(lang, key),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_to_menu_keyboard(lang),
    )

"""Handlers for the informational menu buttons: Services, Pricing, Contact Us."""
import logging

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from keyboards import CB, back_to_menu_keyboard
from mock_data import CONTACT, PRICING, SERVICES

logger = logging.getLogger(__name__)

router = Router()

_CONTENT_BY_CALLBACK = {
    CB.SERVICES: SERVICES,
    CB.PRICING: PRICING,
    CB.CONTACT: CONTACT,
}


@router.callback_query(F.data.in_({CB.SERVICES, CB.PRICING, CB.CONTACT}))
async def show_info(callback: CallbackQuery) -> None:
    """Display mock business info based on which menu button was pressed."""
    await callback.answer()

    text = _CONTENT_BY_CALLBACK.get(callback.data)
    if text is None:
        logger.warning("Unhandled menu callback data: %s", callback.data)
        return

    await callback.message.edit_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_to_menu_keyboard(),
    )

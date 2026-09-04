"""Inline keyboards for the developer portfolio bot."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from i18n import t


class CB:
    LANG_EN = "lang:en"
    LANG_PL = "lang:pl"
    LANG_RU = "lang:ru"
    LANG_UK = "lang:uk"
    CHANGE_LANG = "lang:change"
    ORDER = "menu:order"
    CASES = "menu:cases"
    PRICING = "menu:pricing"
    CONTACT = "menu:contact"
    MAIN_MENU = "menu:main"


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="English", callback_data=CB.LANG_EN),
                InlineKeyboardButton(text="Polski", callback_data=CB.LANG_PL),
            ],
            [
                InlineKeyboardButton(text="Русский", callback_data=CB.LANG_RU),
                InlineKeyboardButton(text="Українська", callback_data=CB.LANG_UK),
            ],
        ]
    )


def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "btn_order"), callback_data=CB.ORDER)],
            [InlineKeyboardButton(text=t(lang, "btn_cases"), callback_data=CB.CASES)],
            [InlineKeyboardButton(text=t(lang, "btn_pricing"), callback_data=CB.PRICING)],
            [InlineKeyboardButton(text=t(lang, "btn_contact"), callback_data=CB.CONTACT)],
            [InlineKeyboardButton(text=t(lang, "btn_language"), callback_data=CB.CHANGE_LANG)],
        ]
    )


def back_to_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "btn_order"), callback_data=CB.ORDER)],
            [InlineKeyboardButton(text=t(lang, "btn_back"), callback_data=CB.MAIN_MENU)],
        ]
    )

"""Keyboard builders and callback-data constants."""
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from i18n import t


class CB:
    """Callback data string constants (avoids magic strings elsewhere)."""

    LANG_EN = "lang:en"
    LANG_PL = "lang:pl"
    CHANGE_LANG = "lang:change"
    NEW_REQUEST = "funnel:new_request"
    CLAIM_BONUS = "funnel:new_request"
    TYPE_PHONE = "funnel:type_phone"
    REVIEWS = "menu:reviews"
    CAT_REPAIR = "cat:repair"
    CAT_CLEANING = "cat:cleaning"
    CAT_OTHER = "cat:other"
    # Kept for backward-compatible callback data if old messages are still open.
    CAT_PLUMBING = "cat:plumbing"
    CAT_ELECTRICAL = "cat:electrical"
    CAT_HANDYMAN = "cat:handyman"
    CAT_GARDEN = "cat:garden"
    SERVICES = "menu:services"
    PRICING = "menu:pricing"
    BOOK = "menu:book"
    CONTACT = "menu:contact"
    MAIN_MENU = "menu:main"


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="English", callback_data=CB.LANG_EN),
                InlineKeyboardButton(text="Polski", callback_data=CB.LANG_PL),
            ]
        ]
    )


def nav_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """Always-visible bottom buttons for /start, /new, /help."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t(lang, "btn_nav_menu")),
                KeyboardButton(text=t(lang, "btn_nav_new")),
                KeyboardButton(text=t(lang, "btn_nav_help")),
            ]
        ],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder=t(lang, "nav_placeholder"),
    )


def nav_button_texts() -> set[str]:
    return {
        t("en", "btn_nav_menu"),
        t("en", "btn_nav_new"),
        t("en", "btn_nav_help"),
        t("pl", "btn_nav_menu"),
        t("pl", "btn_nav_new"),
        t("pl", "btn_nav_help"),
    }


def welcome_funnel_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Conversion screen right after greeting: categories + reviews."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "btn_cat_repair"), callback_data=CB.CAT_REPAIR)],
            [InlineKeyboardButton(text=t(lang, "btn_cat_cleaning"), callback_data=CB.CAT_CLEANING)],
            [InlineKeyboardButton(text=t(lang, "btn_cat_other"), callback_data=CB.CAT_OTHER)],
            [InlineKeyboardButton(text=t(lang, "btn_reviews"), callback_data=CB.REVIEWS)],
            [
                InlineKeyboardButton(text=t(lang, "btn_pricing"), callback_data=CB.PRICING),
                InlineKeyboardButton(text=t(lang, "btn_contact"), callback_data=CB.CONTACT),
            ],
            [InlineKeyboardButton(text=t(lang, "btn_language"), callback_data=CB.CHANGE_LANG)],
        ]
    )


def category_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Same category set used when restarting a request."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "btn_cat_repair"), callback_data=CB.CAT_REPAIR)],
            [InlineKeyboardButton(text=t(lang, "btn_cat_cleaning"), callback_data=CB.CAT_CLEANING)],
            [InlineKeyboardButton(text=t(lang, "btn_cat_other"), callback_data=CB.CAT_OTHER)],
            [InlineKeyboardButton(text=t(lang, "btn_reviews"), callback_data=CB.REVIEWS)],
            [InlineKeyboardButton(text=t(lang, "btn_back"), callback_data=CB.MAIN_MENU)],
        ]
    )


def home_keyboard(lang: str) -> InlineKeyboardMarkup:
    return welcome_funnel_keyboard(lang)


def bonus_keyboard(lang: str) -> InlineKeyboardMarkup:
    return welcome_funnel_keyboard(lang)


def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return welcome_funnel_keyboard(lang)


def back_to_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    """After reviews / info — continue to a request or go home."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "btn_start_request"), callback_data=CB.NEW_REQUEST)],
            [InlineKeyboardButton(text=t(lang, "btn_back"), callback_data=CB.MAIN_MENU)],
        ]
    )

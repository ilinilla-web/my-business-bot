"""Inline keyboard builders and callback-data constants."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class CB:
    """Callback data string constants (avoids magic strings elsewhere)."""

    SERVICES = "menu:services"
    PRICING = "menu:pricing"
    BOOK = "menu:book"
    CONTACT = "menu:contact"
    MAIN_MENU = "menu:main"


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """The primary menu shown on /start and after returning to the menu."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛠️ Services", callback_data=CB.SERVICES)],
            [InlineKeyboardButton(text="💰 Pricing", callback_data=CB.PRICING)],
            [InlineKeyboardButton(text="📅 Book Appointment", callback_data=CB.BOOK)],
            [InlineKeyboardButton(text="📞 Contact Us", callback_data=CB.CONTACT)],
        ]
    )


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """A single 'Back to Menu' button shown under informational screens."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Back to Menu", callback_data=CB.MAIN_MENU)]
        ]
    )

"""Telegram update handlers."""
from aiogram import Dispatcher

from handlers.commands import router as commands_router
from handlers.funnel import router as funnel_router
from handlers.menu import router as menu_router


def setup_routers(dp: Dispatcher) -> None:
    dp.include_router(commands_router)
    dp.include_router(funnel_router)
    dp.include_router(menu_router)

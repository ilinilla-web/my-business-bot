"""Telegram update handlers, grouped by feature."""
from aiogram import Dispatcher

from handlers.booking import router as booking_router
from handlers.commands import router as commands_router
from handlers.funnel import router as funnel_router
from handlers.menu import router as menu_router
from handlers.start import router as start_router


def setup_routers(dp: Dispatcher) -> None:
    """Register all feature routers on the dispatcher."""
    dp.include_router(commands_router)
    dp.include_router(funnel_router)
    dp.include_router(start_router)
    dp.include_router(booking_router)
    dp.include_router(menu_router)

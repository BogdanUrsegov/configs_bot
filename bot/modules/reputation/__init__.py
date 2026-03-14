from .handlers.callbacks import router as callbacks_router
from .handlers.commands import router as commands_router
from aiogram import Router


router = Router()
router.include_routers(
    callbacks_router,
    commands_router
)

__all__ = [
    "router"
]
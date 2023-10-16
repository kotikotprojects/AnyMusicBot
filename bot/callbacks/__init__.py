from aiogram import Router
from . import (
    full_menu,
)
from bot.middlewares import PrivateButtonMiddleware


router = Router()

router.callback_query.middleware(PrivateButtonMiddleware())

router.include_routers(
    full_menu.router,
)

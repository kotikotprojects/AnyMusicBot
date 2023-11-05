from aiogram import Router
from . import (
    full_menu,
    on_home,
    settings,
)
from bot.middlewares import PrivateButtonMiddleware


router = Router()

router.callback_query.middleware(PrivateButtonMiddleware())

router.include_routers(
    full_menu.router,
    on_home.router,
    settings.router,
)

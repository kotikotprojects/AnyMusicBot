from aiogram import Router

from bot.middlewares import PrivateButtonMiddleware, SettingsInjectorMiddleware

from . import full_menu, on_home, settings

router = Router()

router.callback_query.middleware(PrivateButtonMiddleware())
router.callback_query.middleware(SettingsInjectorMiddleware())

router.include_routers(
    full_menu.router,
    on_home.router,
    settings.router,
)

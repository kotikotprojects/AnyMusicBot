from aiogram import Router
from . import (
    initialize,
    inline_song,
    inline_url,
    inline_error,
    inline_default,
    inline_empty,
    on_chosen,
)

from bot.middlewares import SaveChosenMiddleware, SettingsInjectorMiddleware

router = Router()

router.chosen_inline_result.outer_middleware(SaveChosenMiddleware())
router.chosen_inline_result.middleware(SettingsInjectorMiddleware())

router.include_routers(
    initialize.router,
    inline_song.router,
    inline_url.router,
    inline_error.router,
    inline_default.router,
    inline_empty.router,
    on_chosen.router,
)

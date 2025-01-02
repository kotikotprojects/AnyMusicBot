from aiogram import Router

from bot.middlewares import SaveChosenMiddleware, SettingsInjectorMiddleware

from . import (
    initialize,
    inline_default,
    inline_empty,
    inline_error,
    inline_song,
    inline_url,
    on_chosen,
)

router = Router()

router.chosen_inline_result.outer_middleware(SaveChosenMiddleware())
router.chosen_inline_result.middleware(SettingsInjectorMiddleware())
router.inline_query.middleware(SettingsInjectorMiddleware())

router.include_routers(
    initialize.router,
    inline_song.router,
    inline_url.router,
    inline_error.router,
    inline_default.router,
    inline_empty.router,
    on_chosen.router,
)

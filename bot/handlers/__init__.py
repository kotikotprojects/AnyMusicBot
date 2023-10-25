from aiogram import Router
from . import (
    initialize,
    inline_song,
    inline_default,
    inline_empty,
    on_chosen,
)

from bot.middlewares import SaveChosenMiddleware

router = Router()

router.chosen_inline_result.outer_middleware(SaveChosenMiddleware())

router.include_routers(
    initialize.router,
    inline_song.router,
    inline_default.router,
    inline_empty.router,
    on_chosen.router,
)

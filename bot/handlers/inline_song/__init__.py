from aiogram import Router

from . import (
    on_inline_deezer,
    on_inline_soundcloud,
    on_inline_spotify,
    on_inline_youtube,
)

router = Router()
router.include_routers(
    on_inline_spotify.router,
    on_inline_deezer.router,
    on_inline_youtube.router,
    on_inline_soundcloud.router,
)

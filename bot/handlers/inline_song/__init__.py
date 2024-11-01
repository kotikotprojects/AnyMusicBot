from aiogram import Router

from . import (
    on_inline_spotify,
    on_inline_deezer,
    on_inline_youtube,
    on_inline_soundcloud,
)

router = Router()
router.include_routers(
    on_inline_spotify.router,
    on_inline_deezer.router,
    on_inline_youtube.router,
    on_inline_soundcloud.router,
)

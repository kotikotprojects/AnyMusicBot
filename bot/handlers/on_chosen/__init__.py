from aiogram import Router

from . import deezer, recode_cached, soundcloud, spotify, suppress_verify, youtube

router = Router()

router.include_routers(
    spotify.router,
    deezer.router,
    youtube.router,
    soundcloud.router,
    recode_cached.router,
    suppress_verify.router,
)

__all__ = ["router"]

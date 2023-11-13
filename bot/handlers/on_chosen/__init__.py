from aiogram import Router
from . import spotify, deezer, youtube, soundcloud, recode_cached, suppress_verify

router = Router()

router.include_routers(
    spotify.router,
    deezer.router,
    youtube.router,
    soundcloud.router,
    recode_cached.router,
    suppress_verify.router,
)

__all__ = ['router']

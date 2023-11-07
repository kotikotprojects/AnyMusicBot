from aiogram import Router
from . import spotify, deezer, youtube, recode_cached, suppress_verify

router = Router()

router.include_routers(
    spotify.router,
    deezer.router,
    youtube.router,
    recode_cached.router,
    suppress_verify.router,
)

__all__ = ['router']

from aiogram import Router
from . import spotify, deezer, youtube

router = Router()

router.include_routers(
    spotify.router,
    deezer.router,
    youtube.router,
)

__all__ = ['router']

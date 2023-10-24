from aiogram import Router
from . import spotify, deezer

router = Router()

router.include_routers(
    spotify.router,
    deezer.router,
)

__all__ = ['router']

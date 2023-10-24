from .deezer import Deezer
from bot.utils.config import config


deezer = Deezer(
    arl=config.tokens.deezer.arl,
)

__all__ = ['deezer']

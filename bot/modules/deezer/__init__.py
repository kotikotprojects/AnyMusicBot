from bot.utils.config import config

from .deezer import Deezer
from .downloader import DeezerBytestream

deezer = Deezer(
    arl=config.tokens.deezer.arl,
)

__all__ = ["deezer", "DeezerBytestream"]

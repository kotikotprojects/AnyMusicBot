from .deezer import Deezer
from .downloader import DeezerBytestream
from bot.utils.config import config


deezer = Deezer(
    arl=config.tokens.deezer.arl,
)

__all__ = ["deezer", "DeezerBytestream"]

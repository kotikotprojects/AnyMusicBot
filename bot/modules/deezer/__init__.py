from bot.utils import env

from .deezer import Deezer
from .downloader import DeezerBytestream

deezer = Deezer(
    arl=env.DEEZER_ARL,
)

__all__ = ["deezer", "DeezerBytestream"]

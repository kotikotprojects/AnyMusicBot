from bot.utils.config import config

from .downloader import SoundCloudBytestream
from .soundcloud import SoundCloud

soundcloud = SoundCloud(
    client_id=config.tokens.soundcloud.client_id,
)

__all__ = ["soundcloud", "SoundCloudBytestream"]

from .soundcloud import SoundCloud
from .downloader import SoundCloudBytestream
from bot.utils.config import config


soundcloud = SoundCloud(
    client_id=config.tokens.soundcloud.client_id,
)

__all__ = ['soundcloud', 'SoundCloudBytestream']

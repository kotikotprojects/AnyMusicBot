from bot.utils import env

from .downloader import SoundCloudBytestream
from .soundcloud import SoundCloud

soundcloud = SoundCloud(
    client_id=env.SOUNDCLOUD_CLIENT_ID,
)

__all__ = ["soundcloud", "SoundCloudBytestream"]

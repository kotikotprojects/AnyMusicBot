from bot.utils import env

from .spotify import Spotify

spotify = Spotify(
    client_id=env.SPOTIFY_CLIENT_ID,
    client_secret=env.SPOTIFY_CLIENT_SECRET,
)

__all__ = ["spotify"]

from bot.utils.config import config

from .spotify import Spotify

spotify = Spotify(
    client_id=config.tokens.spotify.client_id,
    client_secret=config.tokens.spotify.client_secret,
)

__all__ = ["spotify"]

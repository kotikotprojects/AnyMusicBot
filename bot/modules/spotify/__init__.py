from .spotify import Spotify
from bot.utils.config import config


spotify = Spotify(
    client_id=config.tokens.spotify.client_id,
    client_secret=config.tokens.spotify.client_secret,
)

__all__ = ["spotify"]

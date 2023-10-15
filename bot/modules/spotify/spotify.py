import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from .song import Songs


class Spotify(object):
    def __init__(self, client_id, client_secret):
        self.spotify = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )
        )

        self.songs = Songs(self.spotify)

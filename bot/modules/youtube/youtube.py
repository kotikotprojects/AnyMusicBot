import ytmusicapi

from .song import Songs
from .downloader import Downloader


class YouTube(object):
    def __init__(self):
        self.ytm = ytmusicapi.YTMusic()

        self.download = Downloader
        self.songs = Songs(self.ytm)

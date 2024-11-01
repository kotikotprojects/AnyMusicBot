import ytmusicapi

from .downloader import Downloader
from .song import Songs


class YouTube(object):
    def __init__(self):
        self.ytm = ytmusicapi.YTMusic()

        self.download = Downloader
        self.songs = Songs(self.ytm)

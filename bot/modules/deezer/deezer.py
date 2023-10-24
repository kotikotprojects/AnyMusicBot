import asyncio

from .song import Songs
from .engine import DeezerEngine
from .driver import DeezerDriver
from .downloader import DownloaderBuilder


class Deezer(object):
    def __init__(self, arl: str):
        self.engine = asyncio.get_event_loop().run_until_complete(
            DeezerEngine.from_arl(arl)
        )
        self.driver = DeezerDriver(engine=self.engine)
        self.songs = Songs(driver=self.driver)
        self.downloader = DownloaderBuilder(driver=self.driver)

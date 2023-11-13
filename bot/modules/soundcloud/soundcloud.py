from .engine import SoundCloudEngine
from .driver import SoundCloudDriver
from .song import Songs
from .downloader import DownloaderBuilder


class SoundCloud(object):
    def __init__(self, client_id: str):
        self.engine = SoundCloudEngine(client_id=client_id)
        self.driver = SoundCloudDriver(engine=self.engine)
        self.songs = Songs(driver=self.driver)
        self.downloader = DownloaderBuilder(driver=self.driver)

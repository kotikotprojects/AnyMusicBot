from .downloader import DownloaderBuilder
from .driver import SoundCloudDriver
from .engine import SoundCloudEngine
from .song import Songs


class SoundCloud(object):
    def __init__(self, client_id: str):
        self.engine = SoundCloudEngine(client_id=client_id)
        self.driver = SoundCloudDriver(engine=self.engine)
        self.songs = Songs(driver=self.driver)
        self.downloader = DownloaderBuilder(driver=self.driver)

from typing import Callable

import m3u8
from attrs import define

from .driver import SoundCloudDriver
from .song import SongItem


@define
class SoundCloudBytestream:
    file: bytes
    filename: str
    duration: int
    song: SongItem

    @classmethod
    def from_bytes(cls, bytes_: bytes, filename: str, duration: int, song: SongItem):
        return cls(
            file=bytes_, filename=filename, duration=int(duration / 1000), song=song
        )


@define
class Downloader:
    driver: SoundCloudDriver
    download_url: str
    duration: int
    filename: str
    method: Callable
    song: SongItem

    @classmethod
    async def build(cls, song_id: str, driver: SoundCloudDriver):
        track = await driver.get_track(song_id)
        song = SongItem.from_soundcloud(track)

        if url := cls._try_get_progressive(track["media"]["transcodings"]):
            method = cls._progressive
        else:
            url = track["media"]["transcodings"][0]["url"]
            method = (
                cls._hls
                if (track["media"]["transcodings"][0]["format"]["protocol"] == "hls")
                else cls._progressive
            )

        return cls(
            driver=driver,
            duration=track["duration"],
            method=method,
            download_url=url,
            filename=f'{track["title"]}.mp3',
            song=song,
        )

    @staticmethod
    def _try_get_progressive(urls: list) -> str | None:
        for transcode in urls:
            if transcode["format"]["protocol"] == "progressive":
                return transcode["url"]

    async def _progressive(self, url: str) -> bytes:
        return await self.driver.engine.read_data(
            url=(await self.driver.engine.get(url))["url"]
        )

    async def _hls(self, url: str) -> bytes:
        m3u8_obj = m3u8.loads(
            (
                await self.driver.engine.read_data(
                    (await self.driver.engine.get(url=url))["url"]
                )
            ).decode()
        )

        content = bytearray()
        for segment in m3u8_obj.files:
            content.extend(
                await self.driver.engine.read_data(url=segment, append_client_id=False)
            )

        return content

    async def to_bytestream(self) -> SoundCloudBytestream:
        return SoundCloudBytestream.from_bytes(
            bytes_=await self.method(self, self.download_url),
            filename=self.filename,
            duration=self.duration,
            song=self.song,
        )


@define
class DownloaderBuilder:
    driver: SoundCloudDriver

    async def from_id(self, song_id: str):
        return await Downloader.build(song_id=song_id, driver=self.driver)

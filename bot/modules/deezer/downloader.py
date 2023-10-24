from attrs import define

from io import BytesIO

from .driver import DeezerDriver

from . import track_formats
from .util import UrlDecrypter, ChunkDecrypter
from .song import FullSongItem


@define
class DeezerBytestream:
    file: bytes
    filename: str
    song: FullSongItem

    @classmethod
    def from_bytestream(
            cls,
            bytestream: BytesIO,
            filename: str,
            full_song: FullSongItem
    ):
        bytestream.seek(0)
        return cls(
            file=bytestream.read(),
            filename=filename,
            song=full_song,
        )


@define
class Downloader:
    driver: DeezerDriver
    song_id: int
    track: dict
    song: FullSongItem

    @classmethod
    async def build(
            cls,
            song_id: int,
            driver: DeezerDriver
    ):
        track = await driver.reverse_get_track(song_id)
        return cls(
            song_id=song_id,
            driver=driver,
            track=track['results'],
            song=await FullSongItem.from_deezer(track)
        )

    async def to_bytestream(self) -> DeezerBytestream:
        quality = track_formats.MP3_128

        decrypter = ChunkDecrypter.from_track_id(self.song_id)
        i = 0
        audio = BytesIO()

        async for chunk in self.driver.engine.get_data_iter(
                await self._get_download_url(quality=quality)
        ):
            if i % 3 > 0 or len(chunk) < 2 * 1024:
                audio.write(chunk)
            else:
                audio.write(decrypter.decrypt_chunk(chunk))
            i += 1

        return DeezerBytestream.from_bytestream(
            filename=self.song.full_name + track_formats.TRACK_FORMAT_MAP[quality].ext,
            bytestream=audio,
            full_song=self.song
        )

    async def _get_download_url(self, quality: str = 'MP3_128'):
        md5_origin = self.track["MD5_ORIGIN"]
        track_id = self.track["SNG_ID"]
        media_version = self.track["MEDIA_VERSION"]

        url_decrypter = UrlDecrypter(
            md5_origin=md5_origin,
            track_id=track_id,
            media_version=media_version
        )

        return url_decrypter.get_url_for(track_formats.TRACK_FORMAT_MAP[quality])


@define
class DownloaderBuilder:
    driver: DeezerDriver

    async def from_id(self, song_id: int):
        return await Downloader.build(
            song_id=song_id,
            driver=self.driver
        )
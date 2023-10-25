from attrs import define
import ytmusicapi

from .downloader import Downloader, YouTubeBytestream

from typing import Awaitable

from ..common.song import BaseSongItem


@define
class SongItem(BaseSongItem):
    preview_url: None = None

    @classmethod
    def from_youtube(cls, song_item: dict):
        return cls(
            name=song_item['title'],
            id=song_item['videoId'],
            artists=[artist['name'] for artist in song_item['artists']],
            thumbnail=song_item['thumbnails'][1]['url']
        )

    @classmethod
    def from_details(cls, details: dict):
        return cls(
            name=details['title'],
            id=details['videoId'],
            artists=details['author'].split(' & '),
            thumbnail=details['thumbnail']['thumbnails'][1]['url']
        )

    def to_bytestream(self) -> Awaitable[YouTubeBytestream]:
        return Downloader.from_id(self.id).to_bytestream()


@define
class Songs(object):
    ytm: ytmusicapi.YTMusic

    def search(self, query: str, limit: int = 10) -> list[SongItem] | None:
        r = self.ytm.search(query, limit=limit, filter='songs')

        if r is None:
            return None

        return [SongItem.from_youtube(song_item) for song_item in r]

    def search_one(self, query: str) -> SongItem | None:
        return (self.search(query, limit=1) or [None])[0]

    def from_id(self, song_id: str) -> SongItem | None:
        r = self.ytm.get_song(song_id)

        if r is None:
            return None

        return SongItem.from_details(r['videoDetails'])

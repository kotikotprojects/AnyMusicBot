from attrs import define
import ytmusicapi

from .downloader import Downloader, YouTubeBytestream

from typing import Awaitable


@define
class SongItem:
    name: str
    id: str
    artists: list[str]
    thumbnail: str

    @classmethod
    def from_youtube(cls, song_item: dict):
        return cls(
            name=song_item['title'],
            id=song_item['videoId'],
            artists=[artist['name'] for artist in song_item['artists']],
            thumbnail=song_item['thumbnails'][1]['url']
        )

    @property
    def all_artists(self):
        return ', '.join(self.artists)

    @property
    def full_name(self):
        return f"{self.all_artists} - {self.name}"

    def __str__(self):
        return f"{', '.join(self.artists)} - {self.name}"

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

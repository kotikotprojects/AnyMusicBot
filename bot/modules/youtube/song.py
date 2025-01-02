from typing import Awaitable

import ytmusicapi
from attrs import define

from ..common.song import BaseSongItem
from .downloader import Downloader, YouTubeBytestream


@define
class SongItem(BaseSongItem):
    preview_url: None = None

    @classmethod
    def from_youtube(cls, song_item: dict):
        return cls(
            name=song_item["title"],
            id=song_item["videoId"],
            artists=[artist["name"] for artist in song_item["artists"]],
            thumbnail=song_item["thumbnails"][1]["url"],
        )

    @classmethod
    def from_details(cls, details: dict):
        return cls(
            name=details["title"],
            id=details["videoId"],
            artists=details["author"].split(" & "),
            thumbnail=details["thumbnail"]["thumbnails"][1]["url"],
        )

    def to_bytestream(self) -> Awaitable[YouTubeBytestream]:
        return Downloader.from_id(self.id).to_bytestream()


@define
class Songs(object):
    ytm: ytmusicapi.YTMusic

    def search(
        self, query: str, limit: int = 10, exact_match: bool = False
    ) -> list[SongItem] | None:
        r = self.ytm.search(
            query, limit=limit, filter="songs", ignore_spelling=exact_match
        )

        if r is None:
            return None

        res = []
        [res.append(x) for x in r if x not in res]

        return [SongItem.from_youtube(song_item) for song_item in res]

    def search_one(self, query: str, exact_match: bool = False) -> SongItem | None:
        return (self.search(query, limit=1, exact_match=exact_match) or [None])[0]

    def from_id(self, song_id: str) -> SongItem | None:
        r = self.ytm.get_song(song_id)

        if r is None:
            return None

        return SongItem.from_details(r["videoDetails"])

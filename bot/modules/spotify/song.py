import spotipy
from attrs import define

from ..common.song import BaseSongItem


@define
class SongItem(BaseSongItem):
    @classmethod
    def from_spotify(cls, song_item: dict):
        return cls(
            name=song_item["name"],
            id=song_item["id"],
            artists=[artist["name"] for artist in song_item["artists"]],
            preview_url=(
                song_item["preview_url"].split("?")[0]
                if song_item["preview_url"] is not None
                else None
            ),
            thumbnail=song_item["album"]["images"][1]["url"],
        )


@define
class Songs(object):
    spotify: spotipy.Spotify

    def search(self, query: str, limit: int = 10) -> list[SongItem] | None:
        r = self.spotify.search(query, limit=limit)

        if r is None:
            return None

        return [SongItem.from_spotify(item) for item in r["tracks"]["items"]]

    def from_id(self, song_id: str) -> SongItem | None:
        r = self.spotify.track(song_id)

        if r is None:
            return None

        return SongItem.from_spotify(r)

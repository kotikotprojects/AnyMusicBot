from attrs import define

from ..common.song import BaseSongItem
from .driver import SoundCloudDriver


@define
class SongItem(BaseSongItem):
    @classmethod
    def from_soundcloud(cls, song_item: dict):
        return cls(
            name=song_item["title"],
            id=str(song_item["id"]),
            artists=[],
            thumbnail=(
                song_item["artwork_url"]
                or song_item["user"]["avatar_url"]
                or "https://soundcloud.com/images/default_avatar_large.png"
            ).replace("large.jpg", "t300x300.jpg"),
            preview_url=None,
        )

    @property
    def all_artists(self):
        return None


@define
class Songs(object):
    driver: SoundCloudDriver

    async def search(self, query: str, limit: int = 30) -> list[SongItem] | None:
        r = await self.driver.search(query, limit=limit)

        if r is None:
            return None

        return [SongItem.from_soundcloud(item) for item in r][:limit]

    async def search_one(self, query: str) -> SongItem | None:
        return (await self.search(query, limit=1) or [None])[0]

    async def from_id(self, song_id: str) -> SongItem | None:
        r = await self.driver.get_track(song_id)

        if r is None:
            return None

        return SongItem.from_soundcloud(r)

    async def from_url(self, url: str) -> SongItem | None:
        r = await self.driver.resolve_url(url)

        if r is None:
            return None

        return SongItem.from_soundcloud(r)

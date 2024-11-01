from attrs import define

from .driver import DeezerDriver

from ..common.song import BaseSongItem


@define
class SongItem(BaseSongItem):
    @classmethod
    def from_deezer(cls, song_item: dict):
        return cls(
            name=song_item["title"],
            id=str(song_item["id"]),
            artists=[song_item["artist"]["name"]],
            preview_url=song_item.get("preview"),
            thumbnail=song_item["album"]["cover_medium"],
        )


@define
class FullSongItem(BaseSongItem):
    duration: int
    track_dict: dict

    @classmethod
    async def from_deezer(cls, song_item: dict):
        if song_item.get("results"):
            song_item = song_item["results"]

        return cls(
            name=song_item["SNG_TITLE"],
            id=song_item["SNG_ID"],
            artists=[artist["ART_NAME"] for artist in song_item["ARTISTS"]],
            preview_url=(
                song_item.get("MEDIA").get("HREF")
                if type(song_item.get("MEDIA")) is dict
                and song_item.get("MEDIA").get("TYPE") == "preview"
                else None
            ),
            thumbnail=f"https://e-cdns-images.dzcdn.net/images/cover/"
            f'{song_item["ALB_PICTURE"]}/320x320.jpg',
            duration=int(song_item["DURATION"]),
            track_dict=song_item,
        )


@define
class Songs(object):
    driver: DeezerDriver

    async def search(self, query: str, limit: int = 30) -> list[SongItem] | None:
        r = await self.driver.search(query, limit=limit)

        if r is None:
            return None

        return [SongItem.from_deezer(item) for item in r]

    async def search_one(self, query: str) -> SongItem | None:
        return (await self.search(query, limit=1) or [None])[0]

    async def from_id(self, song_id: str) -> FullSongItem | None:
        r = await self.driver.reverse_get_track(song_id)

        if r is None:
            return None

        return await FullSongItem.from_deezer(r)

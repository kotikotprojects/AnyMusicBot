from attrs import define

from .driver import DeezerDriver


@define
class SongItem:
    name: str
    id: int
    id_s: str
    artist: str
    preview_url: str | None
    thumbnail: str

    @classmethod
    def from_deezer(cls, song_item: dict):
        return cls(
            name=song_item['title'],
            id=song_item['id'],
            id_s=str(song_item['id']),
            artist=song_item['artist']['name'],
            preview_url=song_item.get('preview'),
            thumbnail=song_item['album']['cover_medium']
        )

    @property
    def full_name(self):
        return f"{self.artist} - {self.name}"

    def __str__(self):
        return self.full_name


@define
class FullSongItem:
    name: str
    id: str
    artists: list[str]
    preview_url: str | None
    duration: int
    thumbnail: str
    track_dict: dict

    @classmethod
    async def from_deezer(cls, song_item: dict):
        if song_item.get('results'):
            song_item = song_item['results']

        return cls(
            name=song_item['SNG_TITLE'],
            id=song_item['SNG_ID'],
            artists=[artist['ART_NAME'] for artist in song_item['ARTISTS']],
            preview_url=(song_item.get('MEDIA').get('HREF')
                         if type(song_item.get('MEDIA')) is dict and
                         song_item.get('MEDIA').get('TYPE') == 'preview'
                         else None),
            thumbnail=f'https://e-cdns-images.dzcdn.net/images/cover/'
                      f'{song_item["ALB_PICTURE"]}/320x320.jpg',
            duration=int(song_item['DURATION']),
            track_dict=song_item
        )

    @property
    def all_artists(self):
        return ', '.join(self.artists)

    @property
    def full_name(self):
        return f"{self.all_artists} - {self.name}"

    def __str__(self):
        return self.full_name


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

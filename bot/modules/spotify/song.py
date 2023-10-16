from attrs import define
import spotipy


@define
class SongItem:
    name: str
    id: str
    artists: list[str]
    preview_url: str
    thumbnail: str

    @classmethod
    def from_spotify(cls, song_item: dict):
        return cls(
            name=song_item['name'],
            id=song_item['id'],
            artists=[artist['name'] for artist in song_item['artists']],
            preview_url=song_item['preview_url'].split('?')[0],
            thumbnail=song_item['album']['images'][1]['url']
        )

    @property
    def all_artists(self):
        return ', '.join(self.artists)

    @property
    def full_name(self):
        return f"{self.all_artists} - {self.name}"

    def __str__(self):
        return f"{', '.join(self.artists)} - {self.name}"


@define
class Songs(object):
    spotify: spotipy.Spotify

    def search(self, query: str, limit: int = 10) -> list[SongItem] | None:
        r = self.spotify.search(query, limit=limit)

        if r is None:
            return None

        return [SongItem.from_spotify(item) for item in r['tracks']['items']]

    def from_id(self, song_id: str) -> SongItem | None:
        r = self.spotify.track(song_id)

        if r is None:
            return None

        return SongItem.from_spotify(r)

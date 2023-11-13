from attrs import define


@define
class BaseSongItem:
    name: str
    id: str
    artists: list[str]
    preview_url: str | None
    thumbnail: str

    @property
    def all_artists(self):
        return ', '.join(self.artists)

    @property
    def full_name(self):
        return f"{self.all_artists} - {self.name}" if self.artists else self.name

    def __str__(self):
        return self.full_name

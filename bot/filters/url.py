from urllib.parse import urlparse

from aiogram.filters import BaseFilter
from aiogram.types import InlineQuery


class MusicUrlFilter(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, inline_query: InlineQuery):
        if not inline_query.query.strip().startswith("http"):
            return False

        url = urlparse(inline_query.query)
        return url.scheme in ["http", "https"] and any(
            map(
                url.netloc.endswith,
                [
                    "youtube.com",
                    "youtu.be",
                    "open.spotify.com",
                    "spotify.link",
                    "deezer.page.link",
                    "deezer.com",
                    "soundcloud.com",
                ],
            )
        )

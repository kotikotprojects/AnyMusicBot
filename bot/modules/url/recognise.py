from urllib.parse import urlparse, ParseResult
from dataclasses import dataclass

from typing import Callable, Awaitable, Literal

from bot.modules.database import db
from bot.modules.database.db import DBDict

from bot.modules.youtube import youtube
from bot.modules.spotify import spotify
from bot.modules.deezer import deezer


@dataclass
class RecognisedService:
    name: Literal['yt', 'spot', 'deez']
    db_table: DBDict
    by_id_func: Callable | Awaitable
    parse_result: ParseResult


def recognise_music_service(url: str) -> RecognisedService | None:
    url = urlparse(url)
    if url.netloc.endswith('youtube.com') or url.netloc.endswith('youtu.be'):
        return RecognisedService(
            name='yt',
            db_table=db.youtube,
            by_id_func=youtube.songs.from_id,
            parse_result=url
        )
    elif url.netloc.endswith('open.spotify.com') or url.netloc.endswith('spotify.link'):
        return RecognisedService(
            name='spot',
            db_table=db.spotify,
            by_id_func=spotify.songs.from_id,
            parse_result=url
        )
    elif url.netloc.endswith('deezer.page.link') or url.netloc.endswith('deezer.com'):
        return RecognisedService(
            name='deez',
            db_table=db.deezer,
            by_id_func=deezer.songs.from_id,
            parse_result=url
        )
    else:
        return None

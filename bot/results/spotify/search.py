from aiogram.types import (
    InlineQueryResultDocument, InlineQueryResultCachedAudio
)

from bot.modules.spotify import spotify
from bot.modules.database import db

from ..common.search import get_common_search_result


async def get_spotify_search_results(query: str) -> list[
    InlineQueryResultDocument | InlineQueryResultCachedAudio
]:
    return [
        await get_common_search_result(
            audio=audio,
            db_table=db.spotify,
            service_id='spot'
        )
        for audio in spotify.songs.search(query, limit=50)
    ]

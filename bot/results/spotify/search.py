from aiogram.types import InlineQueryResultCachedAudio, InlineQueryResultDocument

from bot.modules.database import db
from bot.modules.settings import UserSettings
from bot.modules.spotify import spotify

from ..common.search import get_common_search_result


async def get_spotify_search_results(
    query: str, settings: UserSettings
) -> list[InlineQueryResultDocument | InlineQueryResultCachedAudio]:
    return [
        await get_common_search_result(
            audio=audio, db_table=db.spotify, service_id="spot", settings=settings
        )
        for audio in spotify.songs.search(query, limit=50)
    ]

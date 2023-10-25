from aiogram.types import (
    InlineQueryResultDocument, InlineQueryResultCachedAudio
)

from bot.modules.deezer import deezer
from bot.modules.database import db

from ..common.search import get_common_search_result


async def get_deezer_search_results(query: str) -> list[
    InlineQueryResultDocument | InlineQueryResultCachedAudio
]:
    return [
        await get_common_search_result(
            audio=audio,
            db_table=db.deezer,
            service_id='deez'
        )
        for audio in await deezer.songs.search(query, limit=50)
    ]

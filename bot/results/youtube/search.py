from aiogram.types import (
    InlineQueryResultDocument, InlineQueryResultCachedAudio
)

from bot.modules.youtube import youtube
from bot.modules.database import db
from bot.modules.settings import UserSettings

from ..common.search import get_common_search_result


async def get_youtube_search_results(query: str, settings: UserSettings) -> list[
    InlineQueryResultDocument | InlineQueryResultCachedAudio
]:
    return [
        await get_common_search_result(
            audio=audio,
            db_table=db.youtube,
            service_id='yt',
            settings=settings
        )
        for audio in youtube.songs.search(query, limit=40)
    ]

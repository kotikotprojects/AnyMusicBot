from aiogram.types import InlineQueryResultDocument, InlineQueryResultCachedAudio

from bot.modules.soundcloud import soundcloud
from bot.modules.database import db
from bot.modules.settings import UserSettings

from ..common.search import get_common_search_result


async def get_soundcloud_search_results(
    query: str, settings: UserSettings
) -> list[InlineQueryResultDocument | InlineQueryResultCachedAudio]:
    return [
        await get_common_search_result(
            audio=audio, db_table=db.soundcloud, service_id="sc", settings=settings
        )
        for audio in await soundcloud.songs.search(query, limit=50)
    ]

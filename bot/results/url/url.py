from aiogram.types import (
    InlineQueryResultDocument, InlineQueryResultCachedAudio
)

from bot.modules.url import recognise_music_service, get_id
from bot.modules.settings import UserSettings

from ..common.search import get_common_search_result

import inspect


async def get_url_results(query: str, settings: UserSettings) -> list[
    InlineQueryResultDocument | InlineQueryResultCachedAudio
]:
    service = recognise_music_service(query)
    if inspect.iscoroutinefunction(service.by_id_func):
        audio = await service.by_id_func(await get_id(service))
    elif inspect.ismethod(service.by_id_func):
        audio = service.by_id_func(await get_id(service))
    else:
        return []

    return [
        await get_common_search_result(
            audio=audio,
            db_table=service.db_table,
            service_id=service.name,
            settings=settings
        )
    ]

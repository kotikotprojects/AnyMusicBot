from aiogram import Router

from aiogram.types import InlineQuery

from bot.results.spotify import get_spotify_search_results
from bot.filters import ServiceSearchFilter
from bot.modules.settings import UserSettings

router = Router()


@router.inline_query(ServiceSearchFilter("s"))
async def search_spotify_inline_query(
    inline_query: InlineQuery, settings: UserSettings
):
    await inline_query.answer(
        await get_spotify_search_results(
            inline_query.query.removeprefix("s:"), settings
        ),
        cache_time=0,
        is_personal=True,
    )

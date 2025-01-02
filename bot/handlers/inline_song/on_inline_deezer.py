from aiogram import Router
from aiogram.types import InlineQuery

from bot.filters import ServiceSearchFilter
from bot.modules.settings import UserSettings
from bot.results.deezer import get_deezer_search_results

router = Router()


@router.inline_query(ServiceSearchFilter("d"))
async def search_deezer_inline_query(inline_query: InlineQuery, settings: UserSettings):
    await inline_query.answer(
        await get_deezer_search_results(
            inline_query.query.removeprefix("d:"), settings
        ),
        cache_time=0,
        is_personal=True,
    )

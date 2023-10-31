from aiogram import Router

from aiogram.types import InlineQuery

from bot.results.error import get_error_search_results
from bot.filters import ServiceSearchFilter

router = Router()


@router.inline_query(ServiceSearchFilter('error'))
async def search_spotify_inline_query(inline_query: InlineQuery):
    await inline_query.answer(
        await get_error_search_results(inline_query.query.removeprefix('error:')),
        cache_time=0,
        is_personal=True
    )

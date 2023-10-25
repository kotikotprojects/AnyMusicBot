from aiogram import Router

from aiogram.types import InlineQuery

from bot.results.youtube import get_youtube_search_results
from bot.filters import ServiceSearchFilter

router = Router()


@router.inline_query(ServiceSearchFilter('y'))
async def search_youtube_inline_query(inline_query: InlineQuery):
    await inline_query.answer(
        await get_youtube_search_results(inline_query.query.removeprefix('y:')),
        cache_time=0,
        is_personal=True
    )

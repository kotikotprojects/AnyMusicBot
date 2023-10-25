from aiogram import Router

from aiogram.types import InlineQuery

from bot.results.deezer import get_deezer_search_results
from bot.filters import ServiceSearchFilter

router = Router()


@router.inline_query(ServiceSearchFilter('d'))
async def search_deezer_inline_query(inline_query: InlineQuery):
    await inline_query.answer(
        await get_deezer_search_results(inline_query.query.removeprefix('d:')),
        cache_time=0,
        is_personal=True
    )

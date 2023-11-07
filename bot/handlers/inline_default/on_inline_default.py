from aiogram import Router, F

from aiogram.types import InlineQuery

from bot.results.deezer import get_deezer_search_results

from bot.modules.settings import UserSettings

router = Router()


@router.inline_query(F.query != '')
async def default_inline_query(inline_query: InlineQuery, settings: UserSettings):
    await inline_query.answer(
        await get_deezer_search_results(inline_query.query, settings),
        cache_time=0,
        is_personal=True
    )

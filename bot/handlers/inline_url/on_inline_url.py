from aiogram import Router

from aiogram.types import InlineQuery

from bot.results.url import get_url_results
from bot.filters import MusicUrlFilter
from bot.modules.settings import UserSettings

router = Router()


@router.inline_query(MusicUrlFilter())
async def url_deezer_inline_query(inline_query: InlineQuery, settings: UserSettings):
    await inline_query.answer(
        await get_url_results(inline_query.query, settings),
        cache_time=0,
        is_personal=True
    )

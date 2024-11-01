from aiogram import Router

from aiogram.types import InlineQuery

from bot.results.soundcloud import get_soundcloud_search_results
from bot.filters import ServiceSearchMultiletterFilter
from bot.modules.settings import UserSettings

router = Router()


@router.inline_query(ServiceSearchMultiletterFilter(["c", "с"]))
async def search_soundcloud_inline_query(
    inline_query: InlineQuery, settings: UserSettings
):
    await inline_query.answer(
        await get_soundcloud_search_results(
            inline_query.query.removeprefix("c:").removesuffix("с:"), settings
        ),
        cache_time=0,
        is_personal=True,
    )

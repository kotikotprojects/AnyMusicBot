from aiogram import F, Router
from aiogram.types import InlineQuery

from bot.modules.settings import UserSettings
from bot.results.deezer import get_deezer_search_results
from bot.results.soundcloud import get_soundcloud_search_results
from bot.results.spotify import get_spotify_search_results
from bot.results.youtube import get_youtube_search_results

router = Router()


@router.inline_query(F.query != "")
async def default_inline_query(inline_query: InlineQuery, settings: UserSettings):
    await inline_query.answer(
        await {
            "d": get_deezer_search_results,
            "c": get_soundcloud_search_results,
            "y": get_youtube_search_results,
            "s": get_spotify_search_results,
        }[settings["default_search_provider"].value](inline_query.query, settings),
        cache_time=0,
        is_personal=True,
    )

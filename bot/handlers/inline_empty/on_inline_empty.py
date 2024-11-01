from aiogram import Router, F
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle

from bot.keyboards.inline.full_menu import get_full_menu_kb

router = Router()


@router.inline_query(F.query == "")
async def empty_inline_query(inline_query: InlineQuery):
    await inline_query.answer(
        [
            InlineQueryResultArticle(
                id="show_menu",
                title="⚙️ Open menu",
                input_message_content=InputTextMessageContent(message_text="⚙️ Menu"),
                reply_markup=get_full_menu_kb(),
            )
        ],
        cache_time=0,
    )

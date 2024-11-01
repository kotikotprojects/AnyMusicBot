from aiogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from bot.modules.database import db
from bot.modules.error import Error

from bot.common import console


async def get_error_search_results(
    error_id: str,
) -> list[InlineQueryResultArticle] | None:
    error: Error = db.errors.get(error_id)
    if error is None:
        return []

    console.print(f"{error_id} requested")
    console.print(error.traceback)
    console.print(f"-{error_id} requested-")

    return [
        (
            InlineQueryResultArticle(
                id=error_id,
                title=f"Error {error_id}",
                description=error.exception.short,
                input_message_content=InputTextMessageContent(
                    message_text=error.exception.long,
                    parse_mode="HTML",
                ),
            )
        )
    ]

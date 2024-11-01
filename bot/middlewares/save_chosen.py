from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import ChosenInlineResult

from typing import Any, Awaitable, Callable, Dict
from dataclasses import dataclass

from bot.modules.database import db


@dataclass
class SavedUser:
    id: int
    first_name: str
    last_name: str | None
    username: str | None
    language_code: str | None


@dataclass
class SavedResult:
    result_id: str
    from_user: SavedUser
    query: str
    inline_message_id: str


class SaveChosenMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[ChosenInlineResult, Dict[str, Any]], Awaitable[Any]],
        event: ChosenInlineResult,
        data: Dict[str, Any],
    ):
        db.inline[event.inline_message_id] = SavedResult(
            result_id=event.result_id,
            from_user=SavedUser(
                id=event.from_user.id,
                first_name=event.from_user.first_name,
                last_name=event.from_user.last_name,
                username=event.from_user.username,
                language_code=event.from_user.language_code,
            ),
            query=event.query,
            inline_message_id=event.inline_message_id,
        )
        return await handler(event, data)

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import CallbackQuery

from typing import Any, Awaitable, Callable, Dict

from bot.modules.database import db


class PrivateButtonMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ):
        if event.from_user.id == db.inline[event.inline_message_id].from_user.id:
            return await handler(event, data)
        else:
            await event.answer("This button is not for you")

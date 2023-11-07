from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject

from typing import Any, Awaitable, Callable, Dict

from bot.modules.settings import UserSettings


class SettingsInjectorMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ):
        if not hasattr(event, 'from_user'):
            return await handler(event, data)

        settings = UserSettings(event.from_user.id)
        data['settings'] = settings

        return await handler(event, data)

from bot.common import console
from aiogram.types.error_event import ErrorEvent
from aiogram import Bot
from aiogram.dispatcher import router as s_router

from rich.traceback import Traceback
from .pretty import PrettyException

from bot.modules.database import db

from dataclasses import dataclass


@dataclass
class Error:
    exception: PrettyException
    traceback: Traceback
    inline_message_id: str | None = None


async def on_error(event: ErrorEvent, bot: Bot):
    import os
    import base64

    error_id = base64.urlsafe_b64encode(os.urandom(6)).decode()

    traceback = Traceback.from_exception(
        type(event.exception),
        event.exception,
        event.exception.__traceback__,
        show_locals=True,
        suppress=[s_router],
    )
    pretty_exception = PrettyException(event.exception)

    if event.update.chosen_inline_result:
        db.errors[error_id] = Error(
            traceback=traceback,
            exception=pretty_exception,
            inline_message_id=event.update.chosen_inline_result.inline_message_id,
        )

        await bot.edit_message_caption(
            inline_message_id=event.update.chosen_inline_result.inline_message_id,
            caption=f'💔 <b>ERROR</b> occurred. Use this code to get more information: '
                    f'<code>{error_id}</code>',
            parse_mode='HTML',
        )

    else:
        db.errors[error_id] = Error(
            traceback=traceback,
            exception=pretty_exception,
        )

    console.print(f'[red]{error_id} occurred[/]')
    console.print(event)
    console.print(traceback)
    console.print(f'-{error_id} occurred-')

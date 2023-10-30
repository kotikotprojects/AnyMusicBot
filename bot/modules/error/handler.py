from bot.common import console
from aiogram.types.error_event import ErrorEvent
from aiogram import Bot

from rich.traceback import Traceback

from bot.modules.database import db

from dataclasses import dataclass


@dataclass
class Error:
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
        max_frames=1,
    )

    if event.update.chosen_inline_result:
        db.errors[error_id] = Error(
            traceback=traceback,
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
        )

    console.print(f'[red]{error_id} occurred[/]')
    console.print(event)
    console.print(traceback)
    console.print(f'-{error_id}-')

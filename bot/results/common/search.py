from aiogram.types import (
    InlineQueryResultDocument, InlineQueryResultCachedAudio,
    InlineKeyboardMarkup, InlineKeyboardButton
)

from bot.modules.database.db import DBDict

from bot.modules.common.song import BaseSongItem
from typing import TypeVar


BaseSongT = TypeVar('BaseSongT', bound=BaseSongItem)


async def get_common_search_result(
        audio: BaseSongT,
        db_table: DBDict,
        service_id: str
) -> InlineQueryResultDocument | InlineQueryResultCachedAudio:
    return (
        InlineQueryResultDocument(
            id=f'{service_id}::' + audio.id,
            title=audio.name,
            description=audio.all_artists,
            thumb_url=audio.thumbnail,
            document_url=audio.preview_url or audio.thumbnail,
            mime_type='application/zip',
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='Downloading...', callback_data='.')]
                ]
            ),
            caption=audio.full_name,
        ) if audio.id not in list(db_table.keys()) else
        InlineQueryResultCachedAudio(
            id=f'{service_id}c::' + audio.id,
            audio_file_id=db_table[audio.id],
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='Verifying...', callback_data='.')]
                ]
            ),
        )
    )

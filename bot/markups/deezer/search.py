from aiogram.types import (
    InlineQueryResultDocument, InlineQueryResultCachedAudio,
    InlineKeyboardMarkup, InlineKeyboardButton
)

from bot.modules.deezer import deezer
from bot.modules.database import db


async def get_deezer_search_results(query: str) -> list[
    InlineQueryResultDocument | InlineQueryResultCachedAudio
]:
    return [
        InlineQueryResultDocument(
            id='deez::' + audio.id_s,
            title=audio.name,
            description=audio.artist,
            thumb_url=audio.thumbnail,
            document_url=audio.preview_url or audio.thumbnail,
            mime_type='application/zip',
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='Downloading...', callback_data='.')]
                ]
            ),
            caption=audio.full_name,
        ) if audio.id_s not in list(db.deezer.keys()) else
        InlineQueryResultCachedAudio(
            id='deezc::' + audio.id_s,
            audio_file_id=db.deezer[audio.id_s],
        )
        for audio in await deezer.songs.search(query, limit=50)
    ]

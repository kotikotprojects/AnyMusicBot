from aiogram.types import (
    InlineQueryResultDocument, InlineQueryResultCachedAudio,
    InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResult
)

from bot.modules.spotify import spotify
from bot.modules.database import db


async def get_spotify_search_results(query: str) -> list[
    InlineQueryResultDocument | InlineQueryResultCachedAudio
]:
    return [
        InlineQueryResultDocument(
            id='spot::' + audio.id,
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
        ) if audio.id not in list(db.spotify.keys()) else
        InlineQueryResultCachedAudio(
            id='spotc::' + audio.id,
            audio_file_id=db.spotify[audio.id],
        )
        for audio in spotify.songs.search(query, limit=50)
    ]

from aiogram import Router, Bot, F
from aiogram.types import (
    InlineQuery, InlineQueryResultDocument, InlineQueryResultCachedAudio,
    InlineKeyboardMarkup, InlineKeyboardButton,
)

from bot.modules.spotify import spotify
from bot.modules.database import db

router = Router()


@router.inline_query(F.query != '')
async def default_inline_query(inline_query: InlineQuery, bot: Bot):
    await inline_query.answer(
        [
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
                )
            ) if audio.id not in list(db.spotify.keys()) else
            InlineQueryResultCachedAudio(
                id='spotc::' + audio.id,
                audio_file_id=db.spotify[audio.id],
            )
            for audio in spotify.songs.search(inline_query.query)
        ],
        cache_time=0,
        is_personal=True
    )

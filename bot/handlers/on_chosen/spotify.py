from aiogram import Router, Bot, F
from aiogram.types import (
    BufferedInputFile, URLInputFile, InputMediaAudio,
    ChosenInlineResult,
)

from bot.modules.spotify import spotify
from bot.modules.youtube import youtube
from bot.utils.config import config
from bot.modules.database import db

router = Router()


@router.chosen_inline_result(F.result_id.startswith('spot::'))
async def on_new_chosen(chosen_result: ChosenInlineResult, bot: Bot):
    song = spotify.songs.from_id(chosen_result.result_id.removeprefix('spot::'))

    bytestream = youtube.songs.search_one(song.full_name).to_bytestream()

    audio = await bot.send_audio(
        chat_id=config.telegram.files_chat,
        audio=BufferedInputFile(
            file=bytestream.file,
            filename=bytestream.filename,
        ),
        thumbnail=URLInputFile(song.thumbnail),
        performer=song.all_artists,
        title=song.name
    )

    db.spotify[song.id] = audio.audio.file_id

    await bot.edit_message_media(
        inline_message_id=chosen_result.inline_message_id,
        media=InputMediaAudio(media=audio.audio.file_id),
        reply_markup=None
    )

    await db.occasionally_write()

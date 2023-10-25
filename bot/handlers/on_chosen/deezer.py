from aiogram import Router, Bot, F
from aiogram.types import (
    BufferedInputFile, URLInputFile, InputMediaAudio,
    ChosenInlineResult,
)

from bot.modules.deezer import deezer, DeezerBytestream
from bot.utils.config import config
from bot.modules.database import db

router = Router()


@router.chosen_inline_result(F.result_id.startswith('deez::'))
async def on_new_chosen(chosen_result: ChosenInlineResult, bot: Bot):
    bytestream: DeezerBytestream = await (await deezer.downloader.from_id(
        chosen_result.result_id.removeprefix('deez::')
    )).to_bytestream()

    audio = await bot.send_audio(
        chat_id=config.telegram.files_chat,
        audio=BufferedInputFile(
            file=bytestream.file,
            filename=bytestream.filename,
        ),
        thumbnail=URLInputFile(bytestream.song.thumbnail),
        performer=bytestream.song.all_artists,
        title=bytestream.song.name,
        duration=bytestream.song.duration,
    )

    db.deezer[bytestream.song.id] = audio.audio.file_id

    await bot.edit_message_media(
        inline_message_id=chosen_result.inline_message_id,
        media=InputMediaAudio(media=audio.audio.file_id),
        reply_markup=None
    )

    await db.occasionally_write()

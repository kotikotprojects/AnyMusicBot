from aiogram import Router, Bot, F
from aiogram.types import (
    BufferedInputFile, URLInputFile, InputMediaAudio,
    ChosenInlineResult,
)

from bot.modules.spotify import spotify
from bot.modules.youtube import youtube, AgeRestrictedError
from bot.utils.config import config
from bot.modules.database import db

router = Router()


@router.chosen_inline_result(F.result_id.startswith('spot::'))
async def on_new_chosen(chosen_result: ChosenInlineResult, bot: Bot):
    song = spotify.songs.from_id(chosen_result.result_id.removeprefix('spot::'))

    try:
        bytestream = await youtube.songs.search_one(song.full_name).to_bytestream()
    except AgeRestrictedError:
        await bot.edit_message_caption(
            inline_message_id=chosen_result.inline_message_id,
            caption='🔞 This song is age restricted, so I can\'t download it. '
                    'Try downloading it from Deezer or SoundCloud',
            reply_markup=None
        )
        return

    audio = await bot.send_audio(
        chat_id=config.telegram.files_chat,
        audio=BufferedInputFile(
            file=bytestream.file,
            filename=bytestream.filename,
        ),
        thumbnail=URLInputFile(song.thumbnail),
        performer=song.all_artists,
        title=song.name,
        duration=bytestream.duration,
    )

    db.spotify[song.id] = audio.audio.file_id

    await bot.edit_message_media(
        inline_message_id=chosen_result.inline_message_id,
        media=InputMediaAudio(media=audio.audio.file_id),
        reply_markup=None
    )

    await db.occasionally_write()

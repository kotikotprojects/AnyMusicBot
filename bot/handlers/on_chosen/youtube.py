from aiogram import Router, Bot, F
from aiogram.types import (
    BufferedInputFile,
    URLInputFile,
    InputMediaAudio,
    ChosenInlineResult,
)

from bot.modules.youtube import youtube, AgeRestrictedError
from bot.utils.config import config
from bot.modules.database import db
from bot.modules.settings import UserSettings

router = Router()


@router.chosen_inline_result(F.result_id.startswith("yt::"))
async def on_new_chosen(
    chosen_result: ChosenInlineResult, bot: Bot, settings: UserSettings
):
    song = youtube.songs.from_id(chosen_result.result_id.removeprefix("yt::"))

    try:
        bytestream = await song.to_bytestream()
    except AgeRestrictedError:
        await bot.edit_message_caption(
            inline_message_id=chosen_result.inline_message_id,
            caption="🔞 This song is age restricted, so I can't download it. "
            "Try downloading it from Deezer or SoundCloud",
            reply_markup=None,
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

    db.youtube[song.id] = audio.audio.file_id

    await bot.edit_message_media(
        inline_message_id=chosen_result.inline_message_id,
        media=InputMediaAudio(media=audio.audio.file_id),
        reply_markup=None,
    )

    if settings["recode_youtube"].value == "yes":
        await bot.edit_message_caption(
            inline_message_id=chosen_result.inline_message_id,
            caption="🔄 Recoding...",
            reply_markup=None,
        )

        await bytestream.rerender()

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

        db.youtube[song.id] = audio.audio.file_id
        db.recoded[song.id] = True

        await bot.edit_message_media(
            inline_message_id=chosen_result.inline_message_id,
            media=InputMediaAudio(media=audio.audio.file_id),
            reply_markup=None,
        )
    else:
        db.recoded[song.id] = audio.message_id

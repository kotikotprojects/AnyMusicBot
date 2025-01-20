from aiogram import Bot, F, Router
from aiogram.types import (
    BufferedInputFile,
    ChosenInlineResult,
    InputMediaAudio,
    URLInputFile,
)

from bot.modules.database import db
from bot.modules.soundcloud import SoundCloudBytestream, soundcloud
from bot.utils import env

router = Router()


@router.chosen_inline_result(F.result_id.startswith("sc::"))
async def on_new_chosen(chosen_result: ChosenInlineResult, bot: Bot):
    bytestream: SoundCloudBytestream = await (
        await soundcloud.downloader.from_id(
            chosen_result.result_id.removeprefix("sc::")
        )
    ).to_bytestream()

    audio = await bot.send_audio(
        chat_id=env.FILES_CHAT,
        audio=BufferedInputFile(
            file=bytestream.file,
            filename=bytestream.filename,
        ),
        thumbnail=URLInputFile(bytestream.song.thumbnail),
        title=bytestream.song.name,
        duration=bytestream.duration,
    )

    db.soundcloud[bytestream.song.id] = audio.audio.file_id

    await bot.edit_message_media(
        inline_message_id=chosen_result.inline_message_id,
        media=InputMediaAudio(media=audio.audio.file_id),
        reply_markup=None,
    )

from io import BytesIO

from aiogram import Bot, F, Router
from aiogram.types import BufferedInputFile, ChosenInlineResult, InputMediaAudio

from bot.modules.database import db
from bot.modules.settings import UserSettings
from bot.modules.youtube.downloader import YouTubeBytestream
from bot.utils import env

router = Router()


@router.chosen_inline_result(
    F.result_id.startswith("spotc::") | F.result_id.startswith("ytc::")
)
async def on_cached_chosen(
    chosen_result: ChosenInlineResult, bot: Bot, settings: UserSettings
):
    if settings["recode_youtube"].value != "yes":
        await bot.edit_message_reply_markup(
            inline_message_id=chosen_result.inline_message_id, reply_markup=None
        )
        return

    if type(
        db.recoded.get(
            song_id := chosen_result.result_id.removeprefix("spotc::").removeprefix(
                "ytc::"
            )
        )
    ) in [bool, type(None)]:
        await bot.edit_message_reply_markup(
            inline_message_id=chosen_result.inline_message_id, reply_markup=None
        )
        return

    await bot.edit_message_caption(
        inline_message_id=chosen_result.inline_message_id,
        caption="🔄 Recoding...",
        reply_markup=None,
    )

    message = await bot.forward_message(
        env.FILES_CHAT, env.FILES_CHAT, db.recoded[song_id]
    )

    song_io: BytesIO = await bot.download(  # type: ignore
        destination=BytesIO(),
        file=message.audio.file_id,
    )
    await message.delete()

    bytestream = YouTubeBytestream.from_bytestream(
        bytestream=song_io,
        filename=message.audio.file_name,
        duration=message.audio.duration,
    )

    await bytestream.rerender()

    audio = await bot.send_audio(
        chat_id=env.FILES_CHAT,
        audio=BufferedInputFile(
            file=bytestream.file,
            filename=bytestream.filename,
        ),
        thumbnail=BufferedInputFile(
            file=(await bot.download(message.audio.thumbnail.file_id)).read(),
            filename="thumbnail.jpg",
        ),
        performer=message.audio.performer,
        title=message.audio.title,
        duration=bytestream.duration,
    )

    await bot.edit_message_caption(
        inline_message_id=chosen_result.inline_message_id,
        caption="",
        reply_markup=None,
    )
    await bot.edit_message_media(
        inline_message_id=chosen_result.inline_message_id,
        media=InputMediaAudio(media=audio.audio.file_id),
    )

    if chosen_result.result_id.startswith("spotc::"):
        db.spotify[song_id] = audio.audio.file_id
    else:
        db.youtube[song_id] = audio.audio.file_id
    db.recoded[song_id] = True

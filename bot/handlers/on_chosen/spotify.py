from aiogram import Bot, F, Router
from aiogram.types import (
    BufferedInputFile,
    ChosenInlineResult,
    InputMediaAudio,
    URLInputFile,
)

from bot.modules.database import db
from bot.modules.deezer import deezer
from bot.modules.settings import UserSettings
from bot.modules.spotify import spotify
from bot.modules.youtube import AgeRestrictedError, youtube
from bot.modules.youtube.song import SongItem
from bot.utils import env

router = Router()


def not_strict_name(song, yt_song):
    if "feat" in yt_song.name.lower():
        return any(artist.lower() in yt_song.name.lower() for artist in song.artists)
    else:
        return False


@router.chosen_inline_result(F.result_id.startswith("spot::"))
async def on_new_chosen(
    chosen_result: ChosenInlineResult, bot: Bot, settings: UserSettings
):
    song = spotify.songs.from_id(chosen_result.result_id.removeprefix("spot::"))

    bytestream = None
    audio = None

    yt_song: SongItem | None = youtube.songs.search_one(
        song.full_name,
        exact_match=True,
    )
    if settings["exact_spotify_search"].value == "yes":
        if (
            song.all_artists != yt_song.all_artists or song.name != yt_song.name
        ) and not not_strict_name(song, yt_song):
            await bot.edit_message_caption(
                inline_message_id=chosen_result.inline_message_id,
                caption="🙄 Cannot find this song on YouTube, trying Deezer...",
                reply_markup=None,
                parse_mode="HTML",
            )
            yt_song = None
            bytestream = False

    try:
        if bytestream is None:
            bytestream = await yt_song.to_bytestream()

            audio = await bot.send_audio(
                chat_id=env.FILES_CHAT,
                audio=BufferedInputFile(
                    file=bytestream.file,
                    filename=bytestream.filename,
                ),
                thumbnail=URLInputFile(song.thumbnail),
                performer=song.all_artists,
                title=song.name,
                duration=bytestream.duration,
            )
            db.youtube[yt_song.id] = audio.audio.file_id

    except AgeRestrictedError:
        await bot.edit_message_caption(
            inline_message_id=chosen_result.inline_message_id,
            caption="🔞 This song is age restricted, trying Deezer...",
            reply_markup=None,
            parse_mode="HTML",
        )
        yt_song = None

    if not bytestream:
        try:
            deezer_song = await deezer.songs.search_one(
                song.full_name,
            )

            bytestream = await (
                await deezer.downloader.from_id(deezer_song.id)
            ).to_bytestream()

            audio = await bot.send_audio(
                chat_id=env.FILES_CHAT,
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
        except Exception as e:
            assert e

    if audio:
        if settings["exact_spotify_search"].value == "yes":
            db.spotify[song.id] = audio.audio.file_id

        await bot.edit_message_media(
            inline_message_id=chosen_result.inline_message_id,
            media=InputMediaAudio(media=audio.audio.file_id),
            reply_markup=None,
        )

    else:
        await bot.edit_message_caption(
            inline_message_id=chosen_result.inline_message_id,
            caption="🤷‍♂️ Cannot download this song",
            reply_markup=None,
            parse_mode="HTML",
        )

    if yt_song and settings["recode_youtube"].value == "yes":
        await bot.edit_message_caption(
            inline_message_id=chosen_result.inline_message_id,
            caption="🔄 Recoding...",
            reply_markup=None,
            parse_mode="HTML",
        )
        await bytestream.rerender()

        audio = await bot.send_audio(
            chat_id=env.FILES_CHAT,
            audio=BufferedInputFile(
                file=bytestream.file,
                filename=bytestream.filename,
            ),
            thumbnail=URLInputFile(song.thumbnail),
            performer=song.all_artists,
            title=song.name,
            duration=bytestream.duration,
        )
        db.youtube[yt_song.id] = audio.audio.file_id
        db.recoded[yt_song.id] = True

        if settings["exact_spotify_search"].value == "yes":
            db.spotify[song.id] = audio.audio.file_id
            db.recoded[song.id] = True

        await bot.edit_message_caption(
            inline_message_id=chosen_result.inline_message_id,
            caption="",
            reply_markup=None,
        )
        await bot.edit_message_media(
            inline_message_id=chosen_result.inline_message_id,
            media=InputMediaAudio(media=audio.audio.file_id),
        )
    elif yt_song and settings["recode_youtube"].value == "no":
        db.recoded[yt_song.id] = audio.message_id
        if settings["exact_spotify_search"].value == "yes":
            db.recoded[song.id] = audio.message_id

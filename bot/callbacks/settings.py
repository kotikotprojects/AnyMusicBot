from aiogram import Router, Bot
from aiogram.types import (
    CallbackQuery
)

from bot.factories.open_setting import OpenSettingCallback, SettingChoiceCallback

from bot.keyboards.inline.setting import get_setting_kb
from bot.modules.settings import settings_strings, UserSettings

router = Router()


@router.callback_query(OpenSettingCallback.filter())
async def on_settings(
        callback_query: CallbackQuery,
        callback_data: OpenSettingCallback,
        bot: Bot
):
    await bot.edit_message_text(
        inline_message_id=callback_query.inline_message_id,
        text=settings_strings[callback_data.s_id].description,
        reply_markup=get_setting_kb(
            callback_data.s_id,
            str(callback_query.from_user.id)
        )
    )


@router.callback_query(SettingChoiceCallback.filter())
async def on_change_setting(
        callback_query: CallbackQuery,
        callback_data: SettingChoiceCallback,
        bot: Bot
):
    UserSettings(callback_query.from_user.id)[callback_data.s_id] = callback_data.choice
    await bot.edit_message_text(
        inline_message_id=callback_query.inline_message_id,
        text=settings_strings[callback_data.s_id].description,
        reply_markup=get_setting_kb(
            callback_data.s_id,
            str(callback_query.from_user.id)
        )
    )

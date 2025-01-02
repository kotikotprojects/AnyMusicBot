from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.factories.full_menu import FullMenuCallback
from bot.factories.open_setting import OpenSettingCallback
from bot.modules.settings import settings_strings


def get_settings_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=settings_strings[setting_id].name,
                callback_data=OpenSettingCallback(
                    s_id=setting_id,
                ).pack(),
            )
        ]
        for setting_id in settings_strings.keys()
    ] + [
        [
            InlineKeyboardButton(
                text="🔙", callback_data=FullMenuCallback(action="home").pack()
            )
        ]
    ]

    return InlineKeyboardBuilder(buttons).as_markup()

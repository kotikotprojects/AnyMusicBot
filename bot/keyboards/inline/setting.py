from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.factories.full_menu import FullMenuCallback
from bot.factories.open_setting import SettingChoiceCallback
from bot.modules.settings import UserSettings


def get_setting_kb(s_id: str, user_id: str) -> InlineKeyboardMarkup:
    setting = UserSettings(user_id)[s_id]
    buttons = [
        [
            InlineKeyboardButton(
                text=("✅ " if setting.value == choice else "")
                + setting.choices[choice],
                callback_data=SettingChoiceCallback(
                    s_id=s_id,
                    choice=choice,
                ).pack(),
            )
        ]
        for choice in setting.choices.keys()
    ] + [
        [
            InlineKeyboardButton(
                text="🔙", callback_data=FullMenuCallback(action="settings").pack()
            )
        ]
    ]

    return InlineKeyboardBuilder(buttons).as_markup()

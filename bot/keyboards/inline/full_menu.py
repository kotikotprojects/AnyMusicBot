from aiogram.utils.keyboard import (InlineKeyboardMarkup, InlineKeyboardButton,
                                    InlineKeyboardBuilder)
from bot.factories.full_menu import FullMenuCallback


def get_full_menu_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text='⚙️ Settings',
                callback_data=FullMenuCallback(
                    action='settings'
                ).pack()
            ),
            InlineKeyboardButton(
                text='🎵 Search in SoundCloud',
                switch_inline_query_current_chat='sc::'
            )
        ]
    ]

    return InlineKeyboardBuilder(buttons).as_markup()

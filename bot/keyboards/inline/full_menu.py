from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.factories.full_menu import FullMenuCallback
from bot.keyboards.inline import search_variants as sv


def get_full_menu_kb() -> InlineKeyboardMarkup:
    buttons = sv.get_search_variants(
        query="", services=sv.soundcloud | sv.spotify | sv.deezer | sv.youtube
    ) + [
        [
            InlineKeyboardButton(
                text="⚙️ Settings",
                callback_data=FullMenuCallback(action="settings").pack(),
            )
        ],
    ]

    return InlineKeyboardBuilder(buttons).as_markup()

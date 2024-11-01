from typing import Literal
from aiogram.filters.callback_data import CallbackData


class FullMenuCallback(CallbackData, prefix="full_menu"):
    action: Literal["home", "settings"]

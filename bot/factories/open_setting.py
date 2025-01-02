from aiogram.filters.callback_data import CallbackData


class OpenSettingCallback(CallbackData, prefix="setting"):
    s_id: str


class SettingChoiceCallback(CallbackData, prefix="s_choice"):
    s_id: str
    choice: str

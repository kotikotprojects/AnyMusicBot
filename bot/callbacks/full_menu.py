from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from bot.factories.full_menu import FullMenuCallback

from bot.keyboards.inline.settings import get_settings_kb

router = Router()


@router.callback_query(FullMenuCallback.filter(F.action == "settings"))
async def on_settings(callback_query: CallbackQuery, bot: Bot):
    await bot.edit_message_text(
        inline_message_id=callback_query.inline_message_id,
        text="⚙️ Settings",
        reply_markup=get_settings_kb(),
    )

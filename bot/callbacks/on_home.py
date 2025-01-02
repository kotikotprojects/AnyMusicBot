from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery

from bot.factories.full_menu import FullMenuCallback
from bot.keyboards.inline.full_menu import get_full_menu_kb

router = Router()


@router.callback_query(FullMenuCallback.filter(F.action == "home"))
async def on_home(callback_query: CallbackQuery, bot: Bot):
    await bot.edit_message_text(
        inline_message_id=callback_query.inline_message_id,
        text="⚙️ Menu",
        reply_markup=get_full_menu_kb(),
    )

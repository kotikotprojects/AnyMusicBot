from aiogram import Router, Bot, F
from aiogram.types import (
    CallbackQuery
)
from .factories.full_menu import FullMenuCallback

router = Router()


@router.callback_query(FullMenuCallback.filter(F.action == 'settings'))
async def on_close(callback_query: CallbackQuery, bot: Bot):
    await callback_query.answer('Settings are not available yet')

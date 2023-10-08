from aiogram import Bot, Dispatcher
from bot.modules.fsm import InDbStorage
from .utils.config import config

bot = Bot(token=config.telegram.bot_token)
dp = Dispatcher(storage=InDbStorage())

__all__ = ['bot', 'dp', 'config']

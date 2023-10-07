from aiogram import Bot, Dispatcher
from .utils.config import config

bot = Bot(token=config.telegram.bot_token)
dp = Dispatcher()

__all__ = ['bot', 'dp', 'config']

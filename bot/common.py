from aiogram import Bot, Dispatcher
from bot.modules.fsm import InDbStorage
from rich.console import Console
from .utils.config import config

bot = Bot(token=config.telegram.bot_token)
dp = Dispatcher(storage=InDbStorage())
console = Console()


__all__ = ['bot', 'dp', 'config', 'console']

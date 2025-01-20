from aiogram import Bot, Dispatcher
from rich.console import Console

from bot.modules.fsm import InDbStorage

from .utils import env

bot = Bot(token=env.BOT_TOKEN)
dp = Dispatcher(storage=InDbStorage())
console = Console()


__all__ = ["bot", "dp", "console"]

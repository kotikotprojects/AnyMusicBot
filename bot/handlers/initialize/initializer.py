from aiogram import Router, Bot
from rich import print


router = Router()


@router.startup()
async def startup(bot: Bot):
    print(f'[green]Started as[/] @{(await bot.me()).username}')

    from bot.modules.database import pull
    await pull()

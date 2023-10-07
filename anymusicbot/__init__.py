from rich import print


async def runner():
    from .common import dp, bot

    from . import handlers

    dp.include_router(
        handlers.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def main():
    import asyncio

    print('Starting...')
    asyncio.run(runner())

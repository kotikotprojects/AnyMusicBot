from rich import print


async def runner():
    from .common import dp, bot

    from . import handlers, callbacks

    dp.include_routers(
        handlers.router,
        callbacks.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def main():
    import asyncio

    from rich.traceback import install
    install(show_locals=True)

    print('Starting...')
    asyncio.run(runner())

from rich import print
import contextlib


async def runner():
    from .common import dp, bot

    from . import handlers, callbacks
    from .modules.error import on_error

    dp.error.register(on_error)
    dp.include_routers(
        handlers.router,
        callbacks.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def plugins():
    import nest_asyncio
    from rich import traceback
    from icecream import ic

    nest_asyncio.apply()
    traceback.install()
    ic.configureOutput(includeContext=True)


def main():
    import asyncio

    plugins()

    print('Starting...')
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(runner())

    print('[red]Stopped.[/]')

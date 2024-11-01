import contextlib

from rich import print


async def runner():
    from . import callbacks, handlers
    from .common import bot, dp
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
    from icecream import ic
    from rich import traceback

    nest_asyncio.apply()
    traceback.install()
    ic.configureOutput(includeContext=True)


def main():
    import asyncio

    plugins()

    print("Starting...")
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(runner())

    print("[red]Stopped.[/]")

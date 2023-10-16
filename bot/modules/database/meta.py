import os.path
from bot.utils.config import config
from aiogram.exceptions import TelegramBadRequest
import asyncio

from typing import Coroutine

loop = asyncio.get_event_loop()


DBMETA = os.path.join(config.local.db_path, 'dbmeta')
APP_ID = config.local.app_id
DB_CHAT = config.telegram.db_chat


def meta_property(prop_name):
    def getter(self):
        return self[prop_name]

    def setter(self, value):
        self[prop_name] = value

    return property(getter, setter)


class DBMeta:
    app_id = meta_property('app_id')
    message_id = meta_property('message_id')
    update_time = meta_property('update_time')

    def __init__(self):
        if not os.path.isfile(DBMETA):
            open(DBMETA, 'w').write(f'{APP_ID}|None|0')

    def __getitem__(self, item):
        try:
            return open(DBMETA).read().split('|')[{
                "app_id": 0,
                "message_id": 1,
                "update_time": 2
            }.get(item)]
        except TypeError:
            return None

    def __setitem__(self, key, value):
        meta = open(DBMETA).read().split('|')
        meta[{
            "app_id": 0,
            "message_id": 1,
            "update_time": 2
        }[key]] = value
        open(DBMETA, 'w').write('|'.join(str(x) for x in meta))

    def __str__(self):
        return open(DBMETA).read()


def cloud_meta_property(self, prop_name):
    async def getter():
        return await self.get(prop_name)

    return getter()


class CloudMeta:
    def __init__(self):
        def prop_generator(name) -> Coroutine:
            return cloud_meta_property(self, name)

        self.app_id = prop_generator('app_id')
        self.message_id = prop_generator('message_id')
        self.update_time = prop_generator('update_time')

    @staticmethod
    async def get(item):
        from bot.common import bot

        try:
            if not DBMeta().update_time or not bot.cloudmeta_message_text:
                raise AttributeError

        except AttributeError:
            try:
                message = await bot.forward_message(
                    DB_CHAT, DB_CHAT,
                    DBMeta().message_id
                )

                bot.cloudmeta_message_text = message.caption

                await message.delete()

            except TelegramBadRequest:
                print('Cannot get CloudMeta - writing DBDict')
                from .db_model import DBDict
                await DBDict('config').write()
                message = await bot.forward_message(
                    DB_CHAT, DB_CHAT,
                    DBMeta().message_id
                )
                bot.cloudmeta_message_text = message.caption
                await message.delete()

        cloudmeta = bot.cloudmeta_message_text.split('|')
        return cloudmeta[{
            "app_id": 0,
            "message_id": 1,
            "update_time": 2
        }.get(item)]

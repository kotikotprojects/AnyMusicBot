from sqlitedict import SqliteDict
from bot.common import bot
from bot.utils.config import config
from aiogram.types import FSInputFile, InputMediaDocument
from aiogram import exceptions
from pydantic import ValidationError
import time
from .meta import DBMeta
import os.path

DB = os.path.join(config.local.db_path, 'db')
DB_CHAT = config.telegram.db_chat


class DBDict(SqliteDict):
    def __init__(self, tablename: str):
        super().__init__(DB, tablename=tablename, autocommit=True)

    async def write(self):
        try:
            DBMeta().update_time = time.time_ns()

            await bot.edit_message_media(
                media=InputMediaDocument(media=FSInputFile(DB)),
                chat_id=DB_CHAT,
                message_id=DBMeta().message_id
            )
            await bot.edit_message_caption(
                caption=str(DBMeta()),
                chat_id=DB_CHAT,
                message_id=DBMeta().message_id
            )

        except (ValidationError, exceptions.TelegramBadRequest):
            DBMeta().update_time = time.time_ns()

            self['db_message_id'] = (
                await bot.send_document(
                    chat_id=DB_CHAT, document=FSInputFile(DB),
                    disable_notification=True
                )
            ).message_id

            DBMeta().message_id = self['db_message_id']
            await bot.edit_message_caption(
                caption=str(DBMeta()),
                chat_id=DB_CHAT, message_id=self.get('db_message_id')
            )

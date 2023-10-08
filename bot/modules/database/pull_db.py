import os
from .meta import DBMeta, CloudMeta
from bot.common import bot
from bot.utils.config import config
from sqlitedict import SqliteDict

DB = os.path.join(config.local.db_path, 'db')
DB_CHAT = config.telegram.db_chat


async def pull():
    if DBMeta().message_id == 'None':
        from . import db
        print('No dbmeta file')
        if msg_id := db.config.get('db_message_id'):
            print('Found message id in in-db config')
            DBMeta().message_id = msg_id
        await db.write()

    if not os.path.isfile('sync'):
        try:
            if not bot.cloudmeta_message_text:
                print('Cloudmeta initialized incorrectly')
                raise AttributeError
            else:
                return
        except AttributeError:
            if int(DBMeta().update_time) >= int(await CloudMeta().update_time):
                print('DB is up-to-date')
                return
    else:
        print('Database file is new. Trying to download cloud data')
        os.remove('sync')

    print('DB is not up-to-date')

    message = await bot.forward_message(DB_CHAT, DB_CHAT, DBMeta().message_id)

    await message.delete()

    await bot.download(
        message.document,
        destination=DB + 'b'
    )

    from . import db
    for table in db.__dict__.keys():
        new_table = SqliteDict(DB + 'b', tablename=table)
        for key in new_table.keys():
            getattr(db, table)[key] = new_table[key]
        new_table.close()

    await db.write()

    print('Synced')

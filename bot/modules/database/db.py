from .db_model import DBDict
import os.path
from bot.utils.config import config

DB = os.path.join(config.local.db_path, 'db')

if not os.path.isfile(DB):
    open('sync', 'w')


class Db(object):
    def __init__(self):
        self.fsm = DBDict('fsm')
        self.config = DBDict('config')

    async def write(self):
        await self.config.write()

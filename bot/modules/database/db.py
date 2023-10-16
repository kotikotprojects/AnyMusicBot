from .db_model import DBDict
import os.path
from bot.utils.config import config

from random import randint

DB = os.path.join(config.local.db_path, 'db')

if not os.path.isfile(DB):
    open('sync', 'w')


class Db(object):
    def __init__(self):
        self.fsm = DBDict('fsm')
        self.config = DBDict('config')
        self.inline = DBDict('inline')
        self.spotify = DBDict('spotify')

    async def write(self):
        await self.config.write()

    async def occasionally_write(self, chance: int = 5):
        if randint(1, chance) == 1:
            await self.write()

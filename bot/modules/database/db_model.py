from sqlitedict import SqliteDict
from bot.utils.config import config


class DBDict(SqliteDict):
    def __init__(self, tablename: str):
        super().__init__(config.local.db_path, tablename=tablename, autocommit=True)

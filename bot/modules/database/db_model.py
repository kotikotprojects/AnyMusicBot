from sqlitedict import SqliteDict

from bot.utils import env


class DBDict(SqliteDict):
    def __init__(self, tablename: str):
        super().__init__(env.DB_PATH, tablename=tablename, autocommit=True)

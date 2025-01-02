from .db_model import DBDict


class Db(object):
    def __init__(self):
        self.fsm = DBDict("fsm")
        self.config = DBDict("config")
        self.inline = DBDict("inline")
        self.errors = DBDict("errors")
        self.settings = DBDict("settings")
        self.spotify = DBDict("spotify")
        self.deezer = DBDict("deezer")
        self.youtube = DBDict("youtube")
        self.soundcloud = DBDict("soundcloud")
        self.recoded = DBDict("recoded")

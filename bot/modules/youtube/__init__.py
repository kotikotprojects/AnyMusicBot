from pytubefix.exceptions import AgeRestrictedError

from .youtube import YouTube

youtube = YouTube()


__all__ = ["youtube", "AgeRestrictedError"]

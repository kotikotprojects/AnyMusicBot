from .youtube import YouTube
from pytubefix.exceptions import AgeRestrictedError


youtube = YouTube()


__all__ = ["youtube", "AgeRestrictedError"]

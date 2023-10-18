from .youtube import YouTube
from pytube.exceptions import AgeRestrictedError


youtube = YouTube()


__all__ = ['youtube', 'AgeRestrictedError']

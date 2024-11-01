from typing import Union

from shazamio.factory_misc import FACTORY_ARTIST, FACTORY_TRACK
from shazamio.schemas.artists import ArtistInfo, ArtistResponse, ArtistV2
from shazamio.schemas.models import ResponseTrack, TrackInfo, YoutubeData


class Serialize:
    @classmethod
    def track(cls, data):
        return FACTORY_TRACK.load(data, TrackInfo)

    @classmethod
    def youtube(cls, data):
        return FACTORY_TRACK.load(data, YoutubeData)

    @classmethod
    def artist_v2(cls, data) -> ArtistResponse:
        return ArtistResponse.parse_obj(data)

    @classmethod
    def artist(cls, data):
        return FACTORY_ARTIST.load(data, Union[ArtistV2, ArtistInfo])

    @classmethod
    def full_track(cls, data):
        return FACTORY_TRACK.load(data, ResponseTrack)

from dataclasses import dataclass

FLAC = "FLAC"
MP3_128 = "MP3_128"
MP3_256 = "MP3_256"
MP3_320 = "MP3_320"
MP4_RA1 = "MP4_RA1"
MP4_RA2 = "MP4_RA2"
MP4_RA3 = "MP4_RA3"

FALLBACK_QUALITIES = [MP3_320, MP3_128, FLAC]
FORMAT_LIST = [MP3_128, MP3_256, MP3_320, FLAC]


@dataclass
class TrackFormat:
    code: int
    ext: str


TRACK_FORMAT_MAP = {
    FLAC: TrackFormat(
        code=9,
        ext=".flac"
    ),
    MP3_128: TrackFormat(
        code=1,
        ext=".mp3"
    ),
    MP3_256: TrackFormat(
        code=5,
        ext=".mp3"
    ),
    MP3_320: TrackFormat(
        code=3,
        ext=".mp3"
    ),
    MP4_RA1: TrackFormat(
        code=13,
        ext=".mp4"
    ),
    MP4_RA2: TrackFormat(
        code=14,
        ext=".mp4"
    ),
    MP4_RA3: TrackFormat(
        code=15,
        ext=".mp3"
    )
}

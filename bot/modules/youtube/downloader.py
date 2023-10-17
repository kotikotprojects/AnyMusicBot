from attrs import define
from pytube import YouTube, Stream

from pydub import AudioSegment
from io import BytesIO


@define
class YouTubeBytestream:
    file: bytes
    filename: str

    @classmethod
    def from_bytestream(
            cls,
            bytestream: BytesIO,
            filename: str
    ):
        bytestream.seek(0)
        return cls(
            file=bytestream.read(),
            filename=filename
        )

    @property
    def dict(self):
        return {
            "file": self.file,
            "filename": self.filename
        }


@define
class Downloader:
    audio_stream: Stream
    filename: str

    @classmethod
    def from_id(cls, yt_id: str):
        video = YouTube.from_id(yt_id)
        audio_stream = video.streams.filter(
            only_audio=True,
        ).order_by('abr').desc().first()
        return cls(
            audio_stream=audio_stream,
            filename=f'{audio_stream.default_filename}.mp3',
        )

    def to_bytestream(self):
        audio_io = BytesIO()
        self.audio_stream.stream_to_buffer(audio_io)
        audio_io.seek(0)

        return YouTubeBytestream.from_bytestream(
            AudioSegment.from_file(
                file=audio_io
            ).export(BytesIO(), format='mp3', codec='libmp3lame'),
            self.filename,
        )

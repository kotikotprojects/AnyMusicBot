import asyncio
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

from attrs import define
from pydub import AudioSegment
from pytubefix import Stream, YouTube


@define
class YouTubeBytestream:
    file: bytes
    filename: str
    duration: int

    @classmethod
    def from_bytestream(cls, bytestream: BytesIO, filename: str, duration: float):
        bytestream.seek(0)
        return cls(
            file=bytestream.read(),
            filename=filename,
            duration=int(duration),
        )

    def __rerender(self):
        segment = AudioSegment.from_file(file=BytesIO(self.file))

        self.file = segment.export(BytesIO(), format="mp3", codec="libmp3lame").read()
        return self

    async def rerender(self):
        with ThreadPoolExecutor() as executor:
            return await asyncio.get_running_loop().run_in_executor(
                executor, self.__rerender
            )


@define
class Downloader:
    audio_stream: Stream
    filename: str
    duration: int

    @classmethod
    def from_id(cls, yt_id: str):
        video = YouTube.from_id(yt_id)

        audio_stream = (
            video.streams.filter(
                only_audio=True,
            )
            .order_by("abr")
            .desc()
            .first()
        )

        return cls(
            audio_stream=audio_stream,
            filename=f"{audio_stream.default_filename}.mp3",
            duration=int(video.length),
        )

    def __to_bytestream(self):
        audio_io = BytesIO()
        self.audio_stream.stream_to_buffer(audio_io)
        audio_io.seek(0)

        return YouTubeBytestream.from_bytestream(
            audio_io,
            self.filename,
            self.duration,
        )

    async def to_bytestream(self):
        return await asyncio.get_event_loop().run_in_executor(
            None, self.__to_bytestream
        )

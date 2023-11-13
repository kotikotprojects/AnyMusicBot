from attrs import define

from .engine import SoundCloudEngine


@define
class SoundCloudDriver:
    engine: SoundCloudEngine

    async def get_track(self, track_id: int | str):
        return await self.engine.call(
            f'tracks/{track_id}'
        )

    async def search(self, query: str, limit: int = 30):
        return (await self.engine.call(
            'search/tracks',
            params={
                'q': query,
                'limit': limit
            }
        ))['collection']

    async def resolve_url(self, url: str):
        return await self.engine.call(
            'resolve',
            params={
                'url': url
            }
        )

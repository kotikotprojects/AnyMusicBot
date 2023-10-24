from attrs import define

from .engine import DeezerEngine

from .util import clean_query


@define
class DeezerDriver:
    engine: DeezerEngine

    async def get_track(self, track_id: int | str):
        data = await self.engine.call_legacy_api(
            f'track/{track_id}'
        )

        return data

    async def reverse_get_track(self, track_id: int | str):
        return await self.engine.call_api(
            'song.getData',
            params={
                'SNG_ID': str(track_id)
            }
        )

    async def search(self, query: str, limit: int = 30):
        data = await self.engine.call_legacy_api(
            'search/track',
            params={
                'q': clean_query(query),
                'limit': limit
            }
        )

        return data['data']

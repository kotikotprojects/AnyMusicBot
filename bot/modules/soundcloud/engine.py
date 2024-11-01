from attrs import define
import aiohttp


@define
class SoundCloudEngine:
    client_id: str

    async def call(self, request_point: str, params: dict = None):
        return await self.get(
            url=f"https://api-v2.soundcloud.com/{request_point}", params=params
        )

    async def get(self, url: str, params: dict = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                params=(params or {})
                | {
                    "client_id": self.client_id,
                },
            ) as r:
                return await r.json()

    async def read_data(
        self, url: str, params: dict = None, append_client_id: bool = True
    ):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                params=(params or {})
                | (
                    {
                        "client_id": self.client_id,
                    }
                    if append_client_id
                    else {}
                ),
            ) as r:
                return await r.content.read()

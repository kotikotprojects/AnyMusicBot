import aiohttp

from aiohttp import ClientResponse

from attrs import define


HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Content-Language": "en-US",
    "Cache-Control": "max-age=0",
    "Accept": "*/*",
    "Accept-Charset": "utf-8,ISO-8859-1;q=0.7,*;q=0.3",
    "Accept-Language": "en-US,en;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": 'keep-alive'
}


@define
class DeezerEngine:
    cookies: dict
    token: str = None

    @classmethod
    async def from_arl(cls, arl: str):
        cookies = {'arl': arl}
        data, cookies = await cls(cookies).call_api(
            'deezer.getUserData', get_cookies=True
        )

        data = data['results']
        token = data['checkForm']

        return cls(
            cookies=cookies,
            token=token
        )

    async def call_legacy_api(
            self, request_point: str, params: dict = None
    ):
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.get(
                    f"https://api.deezer.com/{request_point}",
                    params=params,
                    headers=HTTP_HEADERS
            ) as r:
                return await r.json()

    @staticmethod
    async def _iter_exact_chunks(response: ClientResponse, chunk_size: int = 2048):
        buffer = b""
        async for chunk in response.content.iter_any():
            buffer += chunk
            while len(buffer) >= chunk_size:
                yield buffer[:chunk_size]
                buffer = buffer[chunk_size:]
        if buffer:
            yield buffer

    async def get_data_iter(self, url: str):
        async with aiohttp.ClientSession(
                cookies=self.cookies,
                headers=HTTP_HEADERS
        ) as session:
            r = await session.get(
                url,
                allow_redirects=True
            )
            async for chunk in self._iter_exact_chunks(r):
                yield chunk

    async def call_api(
            self, method: str, params: dict = None,
            get_cookies: bool = False
    ):
        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with session.post(
                    f"https://www.deezer.com/ajax/gw-light.php",
                    params={
                        'method': method,
                        'api_version': '1.0',
                        'input': '3',
                        'api_token': self.token or 'null',
                    },
                    headers=HTTP_HEADERS,
                    json=params
            ) as r:
                if not get_cookies:
                    return await r.json()
                else:
                    return await r.json(), r.cookies

from .recognise import RecognisedService

import aiohttp


async def get_url_after_redirect(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.head(url, allow_redirects=True) as resp:
            return str(resp.url)


async def get_id(recognised: RecognisedService):
    if recognised.name == "yt":
        return (
            recognised.parse_result.path.replace("/", "")
            if (recognised.parse_result.netloc.endswith("youtu.be"))
            else recognised.parse_result.query.split("=")[1].split("&")[0]
        )

    elif recognised.name == "spot":
        if recognised.parse_result.netloc.endswith("open.spotify.com"):
            return recognised.parse_result.path.split("/")[2]
        else:
            url = await get_url_after_redirect(recognised.parse_result.geturl())
            return url.split("/")[-1].split("?")[0]

    elif recognised.name == "deez":
        if recognised.parse_result.netloc.endswith("deezer.com"):
            return recognised.parse_result.path.split("/")[-1]
        else:
            url = await get_url_after_redirect(recognised.parse_result.geturl())
            return url.split("/")[-1].split("?")[0]

    elif recognised.name == "sc":
        if not recognised.parse_result.netloc.startswith("on"):
            return recognised.parse_result.geturl()
        return await get_url_after_redirect(recognised.parse_result.geturl())

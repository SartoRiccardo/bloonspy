import asyncio
import aiohttp
import http
import random
from typing import Dict, Any
from ..exceptions import BloonsException
from .api import API_URL, check_response


requests_semaphore = asyncio.Semaphore(20)


async def aget(
        client: aiohttp.ClientSession,
        endpoint: str,
        params: Dict[str, Any] = None,
        user_agent: str = "bloonspy Python Library",
) -> list[dict[str, Any]] | dict[str, Any]:
    if params is None:
        params = {}

    retries = 3
    while retries > 0:
        async with requests_semaphore:
            async with client.get(API_URL + endpoint, params=params, headers={"User-Agent": user_agent}) as resp:
                check_response(resp.status, resp.headers.get("content-type").lower())
                if resp.status == http.HTTPStatus.FORBIDDEN and "Retry-After" in resp.headers:
                    retry_after = int(resp.headers["Retry-After"]) + random.random()*3
                    retries -= 1
                    if retries:
                        print(f"[bloonspy] Hit rate limit on {endpoint}. Retry after {retry_after}s")
                    await asyncio.sleep(retry_after)

                data = await resp.json()
                if not data["success"]:
                    raise BloonsException(data["error"])
                return data["body"]

    raise BloonsException(f"Request to {endpoint} failed")


async def aget_lb_page(
        client: aiohttp.ClientSession,
        endpoint: str,
        page_num: int,
        user_agent: str = "bloonspy Python Library",
):
    try:
        return await aget(client, endpoint, params={"page": page_num}, user_agent=user_agent)
    except BloonsException as exc:
        if str(exc) == "No Scores Available":
            return []
        raise exc

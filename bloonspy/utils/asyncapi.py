import asyncio
import aiohttp
import http
import random
from typing import Dict, Any
from ..exceptions import BloonsException
import sys
from .api import API_URL, check_response


requests_locked = False


async def lock_requests(lock_time: float) -> None:
    global requests_locked
    requests_locked = True
    await asyncio.sleep(lock_time)
    requests_locked = False


async def aget(client: aiohttp.ClientSession, endpoint: str, params: Dict[str, Any] = None) -> list[dict[str, Any]] | dict[str, Any]:
    global requests_locked

    if "unittest" in sys.modules.keys():
        print(f"GET {endpoint}, {params=}")

    if params is None:
        params = {}

    while True:
        while requests_locked:
            await asyncio.sleep(random.random()*3+1)

        print(str(client) + "\n\n\n\n\n")
        async with client.get(API_URL + endpoint, params=params, headers={"User-Agent": "bloonspy Python Library"}) as resp:
            check_response(resp.status, resp.headers.get("content-type").lower())
            if resp.status == http.HTTPStatus.FORBIDDEN and "Retry-After" in resp.headers:
                retry_after = int(resp.headers["Retry-After"]) + random.random()*3
                if "unittest" in sys.modules.keys():
                    print(f"Hit rate limit. Retry after {retry_after}s.")

                continue

            data = await resp.json()
            if not data["success"]:
                raise BloonsException(data["error"])
            return data["body"]


async def get_lb_page(endpoint: str, page_num: int):
    try:
        return get(endpoint, params={"page": page_num})
    except BloonsException as exc:
        if str(exc) == "No Scores Available":
            return []
        raise exc

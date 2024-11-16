import requests
import threading
import time
import random
from typing import Dict, Any, List, Union
from ..exceptions import BloonsException, UnderMaintenance
import sys
import http


API_URL = "https://data.ninjakiwi.com"

requests_semaphore = threading.Semaphore(20)


def get(
        endpoint: str,
        params: Dict[str, Any] = None,
        user_agent: str = "bloonspy Python Library",
) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    if "unittest" in sys.modules.keys():
        print(f"GET {endpoint}, {params=}")

    if params is None:
        params = {}

    retries = 3
    while retries > 0:
        with requests_semaphore:
            resp = requests.get(API_URL + endpoint, params=params, headers={"User-Agent": "bloonspy Python Library"})
            check_response(resp.status_code, resp.headers.get("content-type").lower())

            if resp.status_code == 403 and "Retry-After" in resp.headers:
                retry_after = int(resp.headers["Retry-After"]) + random.random() * 3
                retries -= 1
                if retries:
                    print(f"[bloonspy] Hit rate limit on {endpoint}. Retry after {retry_after}s")
                time.sleep(retry_after)

            data = resp.json()
            if not data["success"]:
                raise BloonsException(data["error"])

            return data["body"]

    raise BloonsException(f"Request to {endpoint} failed")


def get_lb_page(
        endpoint: str,
        page_num: int,
        user_agent: str = "bloonspy Python Library",
):
    try:
        return get(endpoint, params={"page": page_num}, user_agent=user_agent)
    except BloonsException as exc:
        if str(exc) == "No Scores Available":
            return []
        raise exc


def check_response(status: int, content_type: str) -> None:
    if status >= 500:
        if status == 525:
            raise UnderMaintenance("Server is under maintenance")

        raise BloonsException("Server error occurred")
    if status >= 400 and not status == http.HTTPStatus.FORBIDDEN:
        raise BloonsException("Bad request")
    if "application/json" not in content_type:
        raise BloonsException("Response is not JSON")

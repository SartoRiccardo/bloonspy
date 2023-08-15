import requests
import threading
import time
import random
from typing import Dict, Any, List, Union
from ..exceptions import BloonsException, UnderMaintenance
import sys


API_URL = "https://data.ninjakiwi.com"

request_lock = None


def lock_requests(lock_time: float) -> None:
    global request_lock
    time.sleep(lock_time)
    request_lock = None


def get(endpoint: str, params: Dict[str, Any] = None) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    global request_lock

    if "unittest" in sys.modules.keys():
        print(f"GET {endpoint}, {params=}")

    if params is None:
        params = {}

    while True:
        while request_lock is not None:
            request_lock.join()

        resp = requests.get(API_URL + endpoint, params=params, headers={"User-Agent": "bloonspy Python Library"})
        if resp.status_code >= 500:
            if "unittest" in sys.modules.keys():
                print(resp.content)
                print(resp.headers)

            if resp.status_code == 525:
                raise UnderMaintenance("Server is under maintenance")

            raise BloonsException("Server error occurred")
        if resp.status_code >= 400:
            if resp.status_code == 403 and "Retry-After" in resp.headers:
                retry_after = int(resp.headers["Retry-After"]) + random.random()*3
                if "unittest" in sys.modules.keys():
                    print(f"Hit rate limit. Retry after {retry_after}s.")
                request_lock = threading.Thread(target=lock_requests, args=(retry_after, ))
                request_lock.start()
                continue

            raise BloonsException("Bad request")
        if "application/json" not in resp.headers.get("content-type").lower():
            raise BloonsException("Response is not JSON")

        data = resp.json()
        if not data["success"]:
            raise BloonsException(data["error"])

        return data["body"]


def get_lb_page(endpoint: str, page_num: int):
    try:
        return get(endpoint, params={"page": page_num})
    except BloonsException as exc:
        if str(exc) == "No Scores Available":
            return []
        raise exc

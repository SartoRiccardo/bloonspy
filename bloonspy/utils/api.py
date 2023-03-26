import requests
from typing import Dict, Any, List, Union
import sys


API_URL = "https://data.ninjakiwi.com"


def get(endpoint: str, params: Dict[str, Any] = None) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    if "unittest" in sys.modules.keys():
        print(f"GET {endpoint}, {params=}")

    if params is None:
        params = {}

    resp = requests.get(API_URL + endpoint, params=params, headers={"User-Agent": "bloonspy Python Library"})
    if resp.status_code >= 500:
        if "unittest" in sys.modules.keys():
            print(resp.content)
            print(resp.headers)
        raise Exception("Server error occurred")
    if resp.status_code >= 400:
        raise Exception("Bad request")
    if "application/json" not in resp.headers.get("content-type").lower():
        raise Exception("Content is not JSON")

    data = resp.json()
    if not data["success"]:
        raise Exception(data["error"])

    return data["body"]


def get_lb_page(endpoint: str, page_num: int):
    try:
        return get(endpoint, params={"page": page_num})
    except Exception as exc:
        if str(exc) == "No Scores Available":
            return []
        raise exc

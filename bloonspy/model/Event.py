from typing import Dict, Any, List
from datetime import datetime
import requests
from ..utils.dictionaries import has_all_keys
from ..utils.decorators import fetch_property
from ..exceptions import NotFound


class Event:
    event_endpoint: str = "https://data.ninjakiwi.com/..."
    event_dict_keys: List[str] = ["name", "start", "end"]
    event_name: str = "event"

    def __init__(self, event_id: str, eager: bool = False, event_json: Dict[str, Any] = None):
        self._id = event_id
        self._data = {}
        self._event_loaded = False

        if event_json and has_all_keys(event_json, self.event_dict_keys):
            self._parse_event(event_json)
        if eager and not self._event_loaded:
            self.load_event()

    def load_event(self, only_if_unloaded: bool = True) -> None:
        if self._event_loaded and only_if_unloaded:
            return

        self._event_loaded = False

        resp = requests.get(self.event_endpoint)
        if resp.status_code != 200:
            return

        data = resp.json()
        if not data["success"]:
            self.handle_exceptions(data["error"])

        event_list = data["body"]
        for event in event_list:
            if event["id"] == self._id:
                self._parse_event(event)
                return

        raise NotFound(f"No {self.event_name} with that ID exists")

    def _parse_event(self, data: Dict[str, Any]) -> None:
        self._data["name"] = data["name"]
        self._data["start"] = datetime.fromtimestamp(data["start"]/1000)
        self._data["end"] = datetime.fromtimestamp(data["end"]/1000)
        self._event_loaded = True

    def handle_exceptions(self, error_msg: str) -> None:
        if error_msg == f"No f{self.event_name} with that ID exists":
            raise NotFound(error_msg)
        raise Exception(error_msg)

    @staticmethod
    def _should_load_property(key_name: str) -> callable:
        def _inner(self: "Event") -> bool:
            return key_name not in self._data
        return _inner

    @property
    def id(self) -> str:
        return self._id

    @property
    @fetch_property(load_event, should_load=_should_load_property("name"))
    def name(self) -> str:
        return self._data["name"]

    @property
    @fetch_property(load_event, should_load=_should_load_property("start"))
    def start(self) -> datetime:
        return self._data["start"]

    @property
    @fetch_property(load_event, should_load=_should_load_property("end"))
    def end(self) -> datetime:
        return self._data["end"]

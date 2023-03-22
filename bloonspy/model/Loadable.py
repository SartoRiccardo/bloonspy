from typing import Dict, Any
import requests


class Loadable:
    endpoint = "{}"

    def __init__(self, resource_id: str, eager: bool = False):
        self._id = resource_id
        self._data = {}
        self._loaded = False
        if eager:
            self.load_resource()

    def load_resource(self, only_if_unloaded: bool = True) -> None:
        if self._loaded and only_if_unloaded:
            return

        resp = requests.get(self.endpoint.format(self._id))
        if resp.status_code != 200:
            return

        data = resp.json()
        if not data["success"]:
            self.handle_exceptions(data["error"])

        self._parse_json(data["body"])

    @staticmethod
    def _should_load_property(key_name: str) -> callable:
        def _inner(self: Loadable) -> bool:
            return key_name not in self._data
        return _inner

    def handle_exceptions(self, error_msg: str) -> None:
        raise Exception(error_msg)

    def _parse_json(self, raw_user: Dict[str, Any]) -> None:
        pass

    @property
    def id(self) -> str:
        return self._id

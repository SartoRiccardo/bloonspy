from typing import Dict, Any
from ..utils.api import get
from ..utils.decorators import exception_handler


class Loadable:
    """Represents a resource that can be loaded."""
    endpoint = "{}"

    def __init__(self, resource_id: str, eager: bool = False):
        self._id = resource_id
        self._data = {}
        self._loaded = False
        if eager:
            self.load_resource()

    def handle_exceptions(self, exception: Exception) -> None:
        return self._handle_exceptions(exception)

    def _handle_exceptions(self, exception: Exception) -> None:
        raise exception

    @exception_handler(handle_exceptions)
    def load_resource(self, only_if_unloaded: bool = True) -> None:
        """Load the resource.

        :param only_if_unloaded: Only make an API call if the resource is unloaded.
            If `False`, it essentially "reloads" the resource.
        :type only_if_unloaded: :class:`bool`

        :raises bloonspy.exceptions.NotFound: If the resource is not found.
        """
        if self._loaded and only_if_unloaded:
            return

        data = get(self.endpoint.format(self._id))
        self._parse_json(data)

    @staticmethod
    def _should_load_property(key_name: str) -> callable:
        def _inner(self: Loadable) -> bool:
            return key_name not in self._data
        return _inner

    def _parse_json(self, raw_user: Dict[str, Any]) -> None:
        self._loaded = True

    @property
    def id(self) -> str:
        """The unique ID of the resource."""
        return self._id

    @property
    def loaded(self) -> bool:
        """`True` if the resource is loaded."""
        return self._loaded

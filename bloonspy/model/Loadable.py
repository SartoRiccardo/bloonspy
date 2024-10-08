from typing import Awaitable, Any
import aiohttp
from ..utils.api import get
from ..utils.asyncapi import aget
from ..utils.decorators import exception_handler
from ..exceptions import NotLoaded


class Loadable:
    """Represents a resource that can be loaded.

    .. container:: operations

       .. describe:: x == y

          Checks if the Event is equal to another Event.
    """
    endpoint = "{}"

    def __init__(
            self,
            resource_id: str,
            eager: bool = False,
            async_client: aiohttp.ClientSession | None = None,
    ):
        self._id = resource_id
        self._data = {}
        self._loaded = False
        self._async_client = async_client
        if eager and self._async_client is None:
            self.load_resource()

    def handle_exceptions(self, exception: Exception) -> None:
        return self._handle_exceptions(exception)

    def _handle_exceptions(self, exception: Exception) -> None:
        raise exception

    @exception_handler(handle_exceptions)
    def load_resource(self, only_if_unloaded: bool = True) -> Awaitable[None] | None:
        """Load the resource.

        :param only_if_unloaded: Only make an API call if the resource is unloaded.
            If `False`, it essentially "reloads" the resource.
        :type only_if_unloaded: :class:`bool`

        :raises bloonspy.exceptions.NotFound: If the resource is not found.
        """
        if self._loaded and only_if_unloaded:
            return

        def on_data_load(data) -> None:
            self._parse_json(data)

        async def async_load() -> None:
            data = await aget(self._async_client, self.endpoint.format(self._id))
            on_data_load(data)

        if self._async_client:
            return async_load()
        on_data_load(get(self.endpoint.format(self._id)))

    @staticmethod
    def _should_load_property(key_name: str) -> callable:
        def _inner(self: Loadable) -> bool:
            return key_name not in self._data
        return _inner

    def _parse_json(self, raw_user: dict[str, Any]) -> None:
        self._loaded = True

    @property
    def id(self) -> str:
        """The unique ID of the resource."""
        return self._id

    @property
    def loaded(self) -> bool:
        """`True` if the resource is loaded."""
        return self._loaded

    def __eq__(self, other):
        return isinstance(other, type(self)) and other.id == self.id

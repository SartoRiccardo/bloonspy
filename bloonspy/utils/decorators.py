from functools import wraps
from ..exceptions import NotLoaded


def fetch_property(loading_func: callable, should_load: callable = None):
    def _decorator(wrapped: callable):
        @wraps(wrapped)
        def wrapper(self, *args, **kwargs):
            if should_load is None or should_load(self):
                if not self.loaded and self._async_client:
                    raise NotLoaded()
                loading_func(self)
            return wrapped(self, *args, **kwargs)
        return wrapper
    return _decorator


def exception_handler(handler: callable) -> callable:
    def _decorator(wrapped: callable) -> callable:
        @wraps(wrapped)
        def wrapper(self, *args, **kwargs):
            try:
                return wrapped(self, *args, **kwargs)
            except Exception as exc:
                handler(self, exc)
        return wrapper
    return _decorator

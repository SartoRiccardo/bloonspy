

def fetch_property(loading_func: callable):
    def _decorator(wrapped: callable):
        def wrapper(self, *args, **kwargs):
            loading_func(self)
            return wrapped(self, *args, **kwargs)
        return wrapper
    return _decorator

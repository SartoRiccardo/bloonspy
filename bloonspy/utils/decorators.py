

def fetch_property(loading_func: callable, should_load: callable = None):
    def _decorator(wrapped: callable):
        def wrapper(self, *args, **kwargs):
            if should_load is None or should_load(self):
                loading_func(self)
            return wrapped(self, *args, **kwargs)
        return wrapper
    return _decorator

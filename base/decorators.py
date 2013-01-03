from django.core.cache import cache
from functools import wraps
from base.cache_keys import PAGECACHE

def pagecache(view_name):
    def pc_decorator(func):
        def wrapper(request, *args, **kwargs):
            response = cache.get(PAGECACHE % view_name)
            if not response:
                response = func(request, *args, **kwargs)
                cache.set(PAGECACHE % view_name, response)
            return response
        return wrapper
    return pc_decorator
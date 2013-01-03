from django.core.cache import cache
from functools import wraps
from base.cache_keys import PAGECACHE

def pagecache(view_name):
    def pc_decorator(func):
        def wrapper(request, *args, **kwargs):
            pc_key = PAGECACHE % ((view_name % kwargs['fb_id']) if 'fb_id' in kwargs else view_name)
            response = cache.get(pc_key)
            if not response:
                response = func(request, *args, **kwargs)
                cache.set(pc_key, response)
            return response
        return wrapper
    return pc_decorator
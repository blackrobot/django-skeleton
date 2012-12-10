from functools import wraps

from django.conf import settings
from django.core.cache import cache


def cache_this(key):
    """ Use this decorator to cache context functions that may use database
    lookups or anything that may cause unnecessary load. It accepts "key" as
    an argument, and an optional keyword argument "timeout" which is in
    seconds.

    >>> @cache_this("example_caching_key", timeout=500)
    >>> def example(request):
    >>>     return { 'foo': "bar" }
    """
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            KEY_PREFIX = "context"
            cache_key = "%s:%s" % (KEY_PREFIX, key)
            data = cache.get(cache_key)
            if not data:
                data = func(*args, **kwargs)
                cache.set(cache_key, data, kwargs.get('timeout', 30 * 60))
            return data
        return inner
    return decorator


def default_context(request):
    """ This provides some default extra context for the templates. """
    return {
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
        'SITE_TITLE': settings.SITE_TITLE,
    }

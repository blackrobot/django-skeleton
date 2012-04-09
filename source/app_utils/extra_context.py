from functools import wraps

from django.conf import settings
from django.core.cache import cache


def cache_this(key):
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


@cache_this("default_extra_context")
def extra_context(request):
    """ This provides some extra context for the templates. """
    return {
        'DEBUG': settings.DEBUG,
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
    }

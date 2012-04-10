from source.settings.defaults import *


DEBUG = LOCAL_SERVE = TEMPLATE_DEBUG = True

EMAIL_HOST = ""
EMAIL_PORT = 1025

SECRET_KEY = "{{ secret_key }}"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "",
        'USER': "",
        'PASSWORD': "",
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 300,
        'BINARY': True,
        'OPTIONS': {'tcp_nodelay': True, 'ketama': True},
    },
}
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

from source.settings.defaults import *


DEBUG = False
LOCAL_SERVE = False

# Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "{{ project_name }}",
        'USER': "",
        'PASSWORD': "",
    },
}

# Caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 300,
        'BINARY': True,
        'OPTIONS': {
            'tcp_nodelay': True,
            'ketama': True,
        },
    },
}

# Only cache for users who aren't logged in
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Paths
PUBLIC_ROOT = get_path(PROJECT_ROOT, '../public/')
MEDIA_ROOT = get_path(PUBLIC_ROOT, 'media/')
STATIC_ROOT = get_path(PUBLIC_ROOT, 'static/')

# Email
EMAIL_HOST = None
EMAIL_HOST_USER = None
EMAIL_HOST_PASSWORD = None
EMAIL_PORT = 25
EMAIL_USE_TLS = False

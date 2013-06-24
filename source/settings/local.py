from .defaults import *


DEBUG = True
LOCAL_SERVE = True

# Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{{ project_name }}',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
    },
}

# Caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
}

# DB backed sessions for development since cache dumps itself
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Paths
PUBLIC_ROOT = get_path(PROJECT_ROOT, '.tmp', 'public')
MEDIA_ROOT = get_path(PUBLIC_ROOT, 'media')
STATIC_ROOT = get_path(PUBLIC_ROOT, 'static')

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# python -m smtpd -n -c DebuggingServer localhost:1025
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025

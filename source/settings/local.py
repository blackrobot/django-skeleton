import os

from source.settings.defaults import *


DEBUG = True
LOCAL_SERVE = True

# Databases
DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.mysql",
        'NAME': "{{ project_name }}",
        'USER': "root",
        'PASSWORD': "root",
    },
}

# Caches
CACHES = {
    'default': {
        'BACKEND': "django.core.cache.backends.dummy.DummyCache",
    },
}

# DB backed sessions for development since cache dumps itself
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# Email
# python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# Fabric
# HOME_DIR is only used for keyfile discovery. Delete this line if using
# an SSH config.
HOME_DIR = os.environ.get('HOME', '~')
FABRIC = {
    # Uncomment these lines if using your SSH config
    # 'USE_SSH_CONFIG': True,
    # 'HOSTS': ["{{ project_name }}"],

    # Delete these lines if using your SSH config
    'USE_SSH_CONFIG': False,
    'HOSTS': ["deploy@%s:22" % SITE_URL],
    'KEY_FILENAME': os.path.join(HOME_DIR, ".ssh/%s.pem" % SITE_URL),
}

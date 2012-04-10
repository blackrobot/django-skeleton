# -*- coding: utf-8 -*-
import os


########################
# MAIN DJANGO SETTINGS #
########################

ADMINS = (
    ("Damon Jablons", 'djablons@blenderbox.com'),
    ("Nick Herro", 'nherro@blenderbox.com'),
    ("Brett Berman", 'bberman@blenderbox.com'),
    ("Caleb Brown", 'cbrown@blenderbox.com'),
)

MANAGERS = ADMINS

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/New_York'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
LANGUAGES = [('en', 'English')]
DEFAULT_LANGUAGE = 0

SITE_ID = 1

USE_I18N = False

USE_L10N = False

# DEBUG should be set in your local settings, it defaults to False
TEMPLATE_DEBUG = DEBUG = False

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# This must be set in your local settings file
SECRET_KEY = None

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    # 3rd Party
    'compressor.finders.CompressorFinder',
)

if USE_I18N:
    TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.i18n',)

ROOT_URLCONF = 'source.urls'

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

#############
# DATABASES #
#############

# Set these up in your local settings file
DATABASES = {
    'default': {
        'ENGINE': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}


#########
# PATHS #
#########

def get_path(*args):
    return os.path.realpath(os.path.join(*args))

PROJECT_DIR = get_path(os.path.dirname(__file__), "../")

LOG_ROOT = get_path(PROJECT_DIR, '../logs')

# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'
MEDIA_ROOT = get_path(PROJECT_DIR, "../", 'media')
STATIC_URL = '/static/'
STATIC_ROOT = get_path(PROJECT_DIR, "../", 'static')
STATICFILES_DIRS = (get_path(PROJECT_DIR, "../public"),)
TEMPLATE_DIRS = (get_path(PROJECT_DIR, "templates"),)
ADMIN_MEDIA_PREFIX = '%sadmin/' % STATIC_URL

# Change this to wherever you want the URL to live
ADMIN_NAMESPACE = "admin"


################
# APPLICATIONS #
################

# Local apps
PROJECT_APPS = (
    'source.app_utils.bootstrap',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',

    # Third Party Django Applications
    'compressor',
    'django_extensions',
    'gunicorn',
    'south',
) + PROJECT_APPS

########################
# APPLICATION SETTINGS #
########################

COMPRESS_ENABLED = True
COMPRESS_PRECOMPILERS = (
    ('text/x-sass', 'sass {infile} {outfile}'),         # Sass
    ('text/x-scss', 'sass --scss {infile} {outfile}'),  # Sass
    ('text/less', 'lessc {infile} {outfile}'),          # Less
)

GOOGLE_ANALYTICS_ID = ''

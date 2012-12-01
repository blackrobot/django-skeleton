import os


# Utility function to join paths
def get_path(*args):
    return os.path.realpath(os.path.join(*args))


# Project Base Path
PROJECT_ROOT = get_path(os.path.dirname(__file__), '../')


##################
# BASIC SETTINGS #
##################

DEBUG = False
TEMPLATE_DEBUG = True

MANAGERS = ADMINS = (
    ("Jane Doe", "jane.doe@example.com"),
    ("John Doe", "john.doe@example.com"),
)

INTERNAL_IPS = (
    '127.0.0.1',
)

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/New_York'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
LANGUAGES = [('en', 'English')]
DEFAULT_LANGUAGE = 0

SITE_ID = 1

SECRET_KEY = "{{ secret_key }}"

# Internationalization and Date Format
USE_I18N = USE_L10N = False

# Template Stuff
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # Django
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',

    # Local
    'source.utils.context_processors.default_context',
)

TEMPLATE_DIRS = (
    get_path(PROJECT_ROOT, 'templates'),
)

MIDDLEWARE_CLASSES = [
    # Django
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # Third Party
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Cache Update and Fetch go first and last respectively
MIDDLEWARE_CLASSES.insert(0, 'django.middleware.cache.UpdateCacheMiddleware')
MIDDLEWARE_CLASSES.append('django.middleware.cache.FetchFromCacheMiddleware')
MIDDLEWARE_CLASSES = tuple(MIDDLEWARE_CLASSES)

# URL Stuff
ROOT_URLCONF = 'source.urls'
ADMIN_NAMESPACE = 'admin'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    # 3rd Party
    'compressor.finders.CompressorFinder',
)

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

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'


#############
# DATABASES #
#############

# Set these in your source/settings/local.py
DATABASES = None
CACHES = None


#########
# PATHS #
#########

# Change these in your source/settings/local.py
MEDIA_URL = '/media/'
MEDIA_ROOT = get_path(PROJECT_ROOT, '../media/')

STATIC_URL = '/static/'
STATIC_ROOT = get_path(PROJECT_ROOT, '../static/')

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

STATICFILES_DIRS = (
    get_path(PROJECT_ROOT, "../public/"),
)


################
# APPLICATIONS #
################

# Local apps
PROJECT_APPS = (
    'source.utils.bootstrap',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # Third Party Django Applications
    'compressor',
    'debug_toolbar',
    'django_extensions',
    'gunicorn',
    'south',
) + PROJECT_APPS


#########
# EMAIL #
#########

DEFAULT_FROM_EMAIL = "no-reply@example.com"
EMAIL_SUBJECT_PREFIX = "[{{ project_name }}]"


########################
# APPLICATION SETTINGS #
########################

HTML_DESIGN_ROOT = get_path(PROJECT_ROOT, "templates/html/")
HTML_DESIGN_NAMESPACE = "html"

COMPRESS_ENABLED = True
COMPRESS_PRECOMPILERS = (
    # Sass
    ('text/x-sass', 'sass {infile} {outfile}'),
    ('text/x-scss', 'sass --scss {infile} {outfile}'),

    # Less
    ('text/less', 'lessc {infile} {outfile}'),
)

GOOGLE_ANALYTICS_ID = ''

# Debug Toolbar
def show_debug_toolbar(request):
    """ Handles logic of showing the debug toolbar. """
    session_key = 'show_debug_toolbar'
    query_key = 'debug'
    # Is this a django admin url?
    in_admin = request.path.startswith('/' + ADMIN_NAMESPACE)

    # If the key is in the url, change the session
    if query_key in request.GET:
        on = request.GET.get(query_key).lower() not in ["off", "false"]
        request.session[session_key] = on

    # Otherwise, default to session or False
    else:
        on = session_key in request.session and request.session[session_key]

    return not in_admin and on


DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': show_debug_toolbar,
    'HIDE_DJANGO_SQL': True,
}

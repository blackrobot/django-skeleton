import os


# Utility function to join paths
def get_path(*args):
    return os.path.realpath(os.path.join(*args))


# Project Base Path
SOURCE_ROOT = get_path(os.path.dirname(__file__), '..')
PROJECT_ROOT = get_path(SOURCE_ROOT, '..')


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

# This will be used in the Django Admin
SITE_TITLE = "{{ project_name|title }}"
SITE_ID = 1
SITE_URL = "example.com"
USE_X_FORWARDED_HOSTS = True
ALLOWED_HOSTS = (
    ".{}".format(SITE_URL),
)

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/New_York'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'
LANGUAGES = [('en', 'English')]
DEFAULT_LANGUAGE = 0

SECRET_KEY = "{{ secret_key }}"

# Internationalization and Date Format
USE_I18N = USE_L10N = False

# Template Stuff
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # Django
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.csrf',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',

    # Local
    'source.utils.context_processors.default_context',
)

TEMPLATE_DIRS = (
    get_path(PROJECT_ROOT, 'templates'),
)

MIDDLEWARE_CLASSES = (
    # Cache Update
    'django.middleware.cache.UpdateCacheMiddleware',

    # Django
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # Cache Fetch
    'django.middleware.cache.FetchFromCacheMiddleware',

    # Third Party
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

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
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
            'filters': ['require_debug_false'],
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'


#############
# DATABASES #
#############

# Set these in your source/settings/local.py
DATABASES = None
CACHES = None
# CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
# CACHE_MIDDLEWARE_ALIAS = 'default'
# CACHE_MIDDLEWARE_SECONDS = 300


###########
# SESSION #
###########

SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2  # Two Weeks
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'


#########
# PATHS #
#########

# Change these in your source/settings/local.py
PUBLIC_ROOT = get_path(PROJECT_ROOT, '..', 'public')

MEDIA_URL = '/media/'
MEDIA_ROOT = get_path(PUBLIC_ROOT, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = get_path(PUBLIC_ROOT, 'static')

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

STATICFILES_DIRS = (
    get_path(PUBLIC_ROOT, 'public'),
)


################
# APPLICATIONS #
################

# Local apps
PROJECT_APPS = (
    # 'source.apps.example',
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

SERVER_EMAIL = DEFAULT_FROM_EMAIL = "no-reply@{}".format(SITE_URL)
EMAIL_SUBJECT_PREFIX = "[{}] ".format(SITE_URL)
EMAIL_HOST = "localhost"
EMAIL_PORT = 25


########################
# APPLICATION SETTINGS #
########################

HTML_DESIGN_ROOT = get_path(SOURCE_ROOT, 'templates', 'html')
HTML_DESIGN_RELATIVE_PATH = 'html'
HTML_DESIGN_NAMESPACE = 'html'

COMPRESS_ENABLED = True
COMPRESS_URL = STATIC_URL
COMPRESS_PRECOMPILERS = (
    # Sass
    ('text/x-sass', 'sass {infile} {outfile}'),
    ('text/x-scss', 'sass --scss {infile} {outfile}'),

    # Less
    ('text/less', 'lessc {infile} {outfile}'),
)
COMPRESS_CSS_FILTERS = (
    'compressor.filters.cssmin.CSSMinFilter',
)
COMPRESS_JS_FILTERS = (
    'compressor.filters.jsmin.JSMinFilter',
)

GOOGLE_ANALYTICS_ID = ''


# Fabric: Override these in local.py as needed
FABRIC_DEFAULTS = {
    'colors': True,
    'use_ssh_config': True,
    'repo': "git@github.com:user/example.git",
    'db_dir': '.tmp/db',
}
FABRIC_BASE_PATH = os.path.join('/', 'var', 'www', '%(site_url)s')
FABRIC_PATH_TEMPLATES = {
    'base': FABRIC_BASE_PATH,
    'app': os.path.join(FABRIC_BASE_PATH, 'app'),
    'backup': os.path.join(FABRIC_BASE_PATH, 'backup'),
    'log': os.path.join(FABRIC_BASE_PATH, 'log'),
    'venv': os.path.join(FABRIC_BASE_PATH, 'env'),
}
FABRIC_ENVIRONMENTS = {
    # 'dev': {
    #     'django_settings': 'source.settings.dev',
    #     'process': 'example.dev',
    #     'site_url': 'example.dev',
    #     'vagrant': True,
    # },

    # 'stage': {
    #     'branch': 'master',
    #     'django_settings': 'source.settings.stage',
    #     'process': 'stage.example.com',
    #     'site_url': 'stage.example.com',
    # },

    # 'prod': {
    #     'branch': 'prod',
    #     'django_settings': 'source.settings.prod',
    #     'process': 'example.com',
    #     'site_url': 'example.com',
    # },
}


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

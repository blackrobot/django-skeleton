import sys

from source.settings.defaults import *


DEBUG = LOCAL_SERVE = TEMPLATE_DEBUG = True

SECRET_KEY = "{{ secret_key }}"

# python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025

if len(set(sys.argv) & set(('test', 'zen'))) > 0:
    # Running tests, so just use a sqlite db
    DATABASES = {
        'default': {
            'ENGINE': "django.db.backends.sqlite3",
            'NAME': "test.db",
        },
    }
else:
    # Real database when not testing
    DATABASES = {
        'default': {
            'ENGINE': "django.db.backends.mysql",
            'NAME': "{{ project_name }}",
            'USER': "",
            'PASSWORD': "",
        },
    }

# Dummy cache for dev
CACHES = {
    'default': {
        'BACKEND': "django.core.cache.backends.dummy.DummyCache",
    },
}

# DB backed sessions for testing since cache dumps itself
SESSION_ENGINE = "django.contrib.sessions.backends.db"

INSTALLED_APPS += (
    'debug_toolbar',
)
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
INTERNAL_IPS = ('127.0.0.1',)


# Debug Toolbar
def show_toolbar(request):
    if 'debug' in request.GET:
        on = request.GET.get('debug') == "on"
        request.session['show_toolbar'] = on
    elif 'show_toolbar' in request.session:
        on = request.session['show_toolbar']
    else:
        on = False
        request.session['show_toolbar'] = on

    return not request.path.startswith(ADMIN_NAMESPACE) and on

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
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    'HIDE_DJANGO_SQL': True,
}

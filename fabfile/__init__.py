import os

from fabric.api import env, task
from fabric.tasks import WrappedCallableTask

from . import (
    setup, utils, vagrant,
    commands as cmd,
    django as dj,
    operations as ops,
)


# Defaults
env.colors = True
env.hosts = ['localhost']
env.use_ssh_config = False

# Get the defaults from the django settings
DEFAULTS = getattr(dj.DJANGO_SETTINGS, 'FABRIC_DEFAULTS', {})
ENVIRONMENTS = getattr(dj.DJANGO_SETTINGS, 'FABRIC_ENVIRONMENTS')
PATH_TEMPLATES = getattr(dj.DJANGO_SETTINGS, 'FABRIC_PATH_TEMPLATES')

if not DEFAULTS:
    utils.error("settings.FABRIC_DEFAULTS is unset")
if not ENVIRONMENTS:
    utils.error("settings.FABRIC_ENVIRONMENTS is unset")
if not PATH_TEMPLATES:
    utils.error("settings.FABRIC_PATH_TEMPLATES is unset")

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Override env values with settings from Django
env.update(DEFAULTS)


def setup_env(key):
    def func():
        env.update(ENVIRONMENTS[key])
        env.update({k: t % env for k, t in PATH_TEMPLATES.iteritems()})
        if env.get('vagrant', False):
            vagrant.configure()

    func.__name__ = key
    func.__doc__ = "The environment setup for %s." % key

    return WrappedCallableTask(func)

# Take the dictionary from settings.FABRIC_ENVIRONMENTS and turn them into
# tasks so you can reference them easily, ie: fab prod operations.pull
globals().update((k, setup_env(k)) for k in ENVIRONMENTS.iterkeys())


# Quick commands
@task
def deploy(static=1, django=1, install=1, nginx=1):
    """ A shortcut to common quick deploy scenario.

    1 Pull the latest from the repo.
    2 Run manage.py collectstatic
    3 If there are pip packages to install, install them.
    4 Restart the Django process
    5 Reload Nginx
    """
    ops.pull()

    if static is 1:
        dj.collectstatic()

    if install is 1 and ops.check_requirements(hide=True):
        ops.install_requirements()

    if django is 1:
        ops.restart_django()

    if nginx is 1:
        ops.reload_nginx()

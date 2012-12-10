from functools import wraps
import os

from fabric.api import cd, env, hide, run as _run, sudo as _sudo, task
from fabric.colors import blue, green, red, yellow
from fabric.contrib import django

django.settings_module('source.settings.local')
from django.conf import settings


#####################
# ENVIRONMENT SETUP #
#####################

config = settings.FABRIC

env.use_ssh_config = config['USE_SSH_CONFIG']
env.hosts = config['HOSTS']

if not env.use_ssh_config:
    env.key_filename = config['KEY_FILENAME']

# Defaults
env.www_dir = "/var/www/"
env.colors = True


def get_paths(sub_dir):
    """ Given the sub-directory, this returns a 3-tuple of the base path
    of the project, the app path, and the environment path.
    """
    base_dir = os.path.join(env.www_dir, sub_dir, '/')
    app_dir = os.path.join(base_dir, "app/")
    env_dir = os.path.join(base_dir, "env/")
    return base_dir, app_dir, env_dir


@task
def prod():
    """ Sets up the environment for production. """
    # Set the website's URL in your django settings
    env.site_url = "example.com"

    # Default paths
    env.base, env.app, env.venv = get_paths(env.site_url)

    env.process = env.site_url


###################
# LOCAL UTILITIES #
###################

def log_call(func):
    @wraps(func)
    def logged(*args, **kawrgs):
        name = func.__name__.replace('_', ' ').title()
        line = "-" * len(name)
        out = ""

        for val in [name, line]:
            out += "\n   %s" % val
        print green(out)

        return func(*args, **kawrgs)
    return logged


def print_command(command):
    print "   %s %s %s\n" % (blue('$', bold=True),
                             yellow(command, bold=True),
                             red('->', bold=True))


##############
# MAIN TASKS #
##############

@task
def run(command, show=True):
    """ Runs a shell command on the remote server. """
    if show:
        print_command(command)

    with hide("running"):
        return _run(command)


@task
def sudo(command, show=True):
    """ Runs a command as sudo. """
    if show:
        print_command(command)

    with hide("running"):
        return _sudo(command)


@task
def python(command):
    """ Runs a command with the environment's python binary. """
    _python = os.path.join(env.venv, "bin/python")
    return run("%s %s" % (_python, command))


@task
def manage(command):
    """ Run a django management command. """
    with cd(os.path.join(env.app, "source/")):
        return python("manage.py %s" % command)


@task
def git(command):
    """ Run a git command on the remote server. """
    with cd(env.app):
        return run("git %s" % command)


@task
def pip(command):
    """ Runs pip in the environment with the given command. """
    _pip = os.path.join(env.venv, "bin/pip")
    return run("%s %s" % (_pip, command))


@task
def nginx(command):
    """ Runs an Nginx command. """
    return sudo("service nginx %s" % command)


@task
def supervisor(command):
    """ Runs an supervisor command. """
    return sudo("supervisorctl %s" % command)


#################
# SPECIAL TASKS #
#################

@task
@log_call
def collect_static():
    """ Collects all of the static media. """
    return manage("collectstatic --noinput")


@task
@log_call
def install_requirements():
    """ Installs the requirements from the requirements.txt file. This will run
    as the deploy user if on dev.
    """
    with cd(env.app):
        return pip("install -r requirements.txt")


@task
@log_call
def migrate_db():
    """ Migrates the db. """
    return manage("migrate --all")


@task
@log_call
def pull():
    """ Git pulls on the remote host. """
    return git("pull")


@task
@log_call
def reload_nginx():
    """ Restarts the nginx process. """
    return nginx("reload")


@task
@log_call
def restart_django():
    """ Restarts the Django Supervisor process. """
    return supervisor("restart %(process)s" % env)


@task
@log_call
def restart_celery():
    """ Restarts the Celery Supervisor process. """
    return supervisor("restart celery")


@task
@log_call
def restart_memcached():
    """ Restarts the Memcached server. """
    return sudo("service memcached restart")


@task
@log_call
def clear_cache():
    """ Clears the cache. """
    return manage('clear_cache')


@task
@log_call
def deploy(clear=None, install=None, migrate=None, nginx=None, static=None):

    # Always pull
    pull()

    if install:
        install_requirements()

    if static:
        collect_static()

    if clear:
        clear_cache()

    if migrate:
        migrate_db()

    # Always restart
    restart_django()

    if reload_nginx:
        reload_nginx()

import importlib
import os
import sys

# Adjust the path
sys.path.append(os.path.join(os.path.abspath('..')))
_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE', 'source.settings')
DJANGO_SETTINGS = importlib.import_module(_MODULE)

from fabric.api import cd, env, task

from .commands import python, get_binary
from .utils import log_call, run


__all__ = [
    'DJANGO_SETTINGS', 'get_settings', 'manage', 'clear_cache', 'compress',
    'collectstatic', 'dbshell', 'load_fixtures', 'migrate', 'rebuild_index',
    'rsync_media', 'runserver', 'syncdb', 'update_index',
]


MANAGE = "manage.py"


def get_settings(module):
    """ This retrieves the django settings for the given module. """
    return importlib.import_module(module)


@task
def manage(args=""):
    """ Run a django management command with the given arguments. """
    if env.get("django_settings", False):
        args += " --settings=%(django_settings)s" % env

    with cd(env.app):
        python("%s %s" % (MANAGE, args))


@task
@log_call
def clear_cache():
    """ Clears the cache. """
    manage("clear_cache")


@task
@log_call
def collectstatic():
    """ Collects all of the static media. """
    manage("collectstatic --noinput")


@task
@log_call
def compress():
    """ Compresses js and css files. """
    manage("compress")


@task
@log_call
def dbshell(args=""):
    """ Accepts a string `args`, and pipes it to the django dbshell command.
    """
    with cd(env.app):
        run("%s | %s %s dbshell" % (args, get_binary('python'), MANAGE))


@task
@log_call
def load_fixtures(fixtures=None):
    """ This will load fixtures. """
    to_load = fixtures.split(' ') if fixtures else env.fixtures
    for fixture in to_load:
        manage("loaddata %s" % fixture)


@task
@log_call
def migrate(args="--all"):
    """ Migrates the db. """
    manage("migrate %s" % args)


@task
@log_call
def rebuild_index():
    """ Reindexes the Haystack index. """
    manage("rebuild_index --noinput")


@task
@log_call
def runserver(plus=0):
    cmd = 'runserver_plus' if plus is not 0 else 'runserver'
    manage(cmd)


@task
@log_call
def rsync_media():
    """ This will rsync your local media root with the remote media root. """
    import operations
    local_path = DJANGO_SETTINGS.MEDIA_ROOT
    local_parts = local_path.split('/')
    remote_parts = get_settings(env.django_settings).MEDIA_ROOT.split('/')

    # Fix remote media path
    for i in range(len(remote_parts)):
        if remote_parts[i] != local_parts[i]:
            remote_path = os.path.join(env.base, *remote_parts[i:]) + '/'
            break

    operations.rsync(remote_path, local_path, log=False)


@task
@log_call
def syncdb(command=""):
    """ Runs syncdb, including an argument string if passed. """
    return manage("syncdb --noinput %s" % command)


@task
@log_call
def update_index(remove=1, age=None):
    """ Reindexes the Haystack index. """
    args = []

    if remove is 1:
        args.append("--remove")

    if age:
        args.append("--age=%s" % age)

    manage("update_index %s" % ' '.join(args))

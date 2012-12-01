from functools import wraps
from os import path

from fabric.api import cd, env, hide, run as _run, sudo as _sudo, task
from fabric.colors import blue, green, red, yellow


#####################
# ENVIRONMENT SETUP #
#####################
env.use_ssh_config = True
env.colors = True

# This should be what the Host is called in your ~/.ssh/config
env.hosts = ["{{ project_name }}"]
env.www_dir = "/var/www/"

@task
def prod():
    """ Sets up the environment for production. """

    # This is where the project lives on the server
    env.base = path.join(env.www_dir, "{{ project_url }}/")

    env.app = path.join(env.base, "app/")
    env.venv = path.join(env.base, "env/")
    env.backup = path.join(env.base, "backup/")

    env.process = "{{ project_url }}"


@task
def stage():
    """ Sets up the environment for devlopment. """
    env.base = path.join(env.www_dir, "stage.{{ project_url }}/")

    env.app = path.join(env.base, "app/")
    env.venv = path.join(env.base, "env/")

    env.process = "stage.{{ project_url }}"


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
    _python = path.join(env.venv, "bin/python")
    return run("%s %s" % (_python, command))


@task
def manage(command):
    """ Run a django management command. """
    with cd(path.join(env.app, "source/")):
        return python("manage.py %s" % command)


@task
def git(command):
    """ Run a git command on the remote server. """
    with cd(env.app):
        return run("git %s" % command)


@task
def pip(command):
    """ Runs pip in the environment with the given command. """
    _pip = path.join(env.venv, "bin/pip")
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

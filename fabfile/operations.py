# -*- coding: utf-8 -*-

import datetime
import os

from fabric.api import cd, env, get, hide, local, settings, task
from fabric.colors import blue, green, white, yellow
from fabric.contrib.console import confirm
from fabric.utils import indent, puts

from .commands import git, nginx, pip, supervisor
from .django import DJANGO_SETTINGS, get_settings
from .utils import error, log_call, run, sudo, warning


__all__ = [
    'mysql_command', 'check_requirements', 'check_nginx', 'db_create',
    'db_drop', 'db_dump', 'db_restore', 'install_requirements', 'pull',
    'restart_celery', 'restart_django', 'restart_memcached', 'reload_nginx',
    'restart', 'tailgun', 'timestamp',
]


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_EXT = 'sql'


@task
def check_requirements(hide=False):
    """ This checks if the installed packages are different from those in the
    requirements.txt file.
    """
    command = "diff requirements.txt <(%s)" % pip("freeze", execute=False)

    with cd(env.app):
        out = run(command, quiet=True, show=False).strip()

        if hide:
            return out

        if out:
            diff = indent(out.splitlines(), strip=True)
            warning(["Installed packages are different from the "
                     "requirements.txt file:"] + diff)


def mysql_command(append=None, db=None, execute=None, **kwargs):
    """ This takes a list of strings as the first argument, a django styled
    dictionary of django database settings, and keyword arguments representing
    the context for string replacement. It then returns a rendered string
    filled with variables from the db, and appends the space-joined
    list of strings from the first argument.
    """
    context = {}
    if not db:
        db = DJANGO_SETTINGS.DATABASES['default']
    context.update(db)
    context.update(kwargs)

    args = [a for a in ('USER', 'PASSWORD', 'HOST', 'PORT') if a in context]
    opts = ["--%s={%s}" % (a.lower(), a) for a in args]

    if execute:
        if execute[0] not in ('"', "'"):
            execute = '"{}"'.format(execute)
        opts.extend(['-e', execute])
    else:
        opts.append('{NAME}')

    cmd = ' '.join(opts + (append or [])).format(**context)

    return cmd


def get_dir(path):
    """ This looks for the given path, prefixed with the project path if
    relative. If it doesn't exist, it creates it and caches it. It then
    returns the full absolute path to the directory as a string. For safety
    it will not attempt to create any directories which are not relative
    to the base project dir.
    """
    if not path.startswith('/'):
        path = os.path.abspath(os.path.join(BASE_DIR, path))

    if path.startswith(BASE_DIR) and not os.path.exists(path):
        os.makedirs(path)

    return path


@task
@log_call
def db_create(charset='utf8', collate='utf8_general_ci'):
    """ This will create your local database. """
    cmd = "CREATE DATABASE {NAME} CHARACTER SET {charset} COLLATE {collate};"
    local('mysql {}'.format(mysql_command(
        execute=cmd, charset=charset, collate=collate)))


@task
@log_call
def db_drop(confirmed="no"):
    """ This will drop your local database. Pass "yes" or "y" to skip the
    confirmation.
    """
    conf = confirmed.lower() in ["yes", "y"]

    if not conf:
        warning("You are about to drop your local MySQL database '{}'!".format(
                DJANGO_SETTINGS.DATABASES['default']['NAME']))
        if not confirm("Are you sure?", default=False):
            return

    local('mysql {}'.format(mysql_command(execute='DROP DATABASE {NAME};')))


@task
@log_call
def db_restore():
    """ By default, this will download the latest PSQL dump from the server
    and install it locally. If filename is given, this will download and
    restore the dump at the given filename.
    """
    tmp = os.path.join(get_dir(env.db_dir), '*.sql.bz2')
    filename = local('ls -t {} | head -1'.format(tmp), capture=True).strip()
    cmd = 'bunzip2 < {} | mysql {}'.format(filename, mysql_command())
    local(cmd)


@task
@log_call
def db_dump():
    """ This will download a MySQL database from the remote server. """
    db = get_settings(env.django_settings).DATABASES['default']
    remote_path = os.path.join(env.backup, '{}.{}.sql.bz2').format(
        db['NAME'],
        datetime.datetime.now().strftime('%Y-%m-%d.%H%M%S'),
    )
    # Run the MySQL dump command piped to the Bzip command
    run('mysqldump {} | bzip2 > {}'.format(mysql_command(db=db), remote_path))
    # Download the Bzip file we just created
    get(remote_path, local_path=get_dir(env.db_dir))


@task
@log_call
def install_requirements():
    """ Installs the requirements from the requirements.txt file. This will run
    as the deploy user if on dev.
    """
    with cd(env.app):
        pip("install -r requirements.txt")


@task
@log_call
def pull():
    """ Git pulls on the remote host. """
    git("pull")


@task
@log_call
def restart_celery():
    """ Restarts the Celery Supervisor process. """
    supervisor("restart celery")


@task
@log_call
def restart_django():
    """ Restarts the Django Supervisor process. """
    supervisor("restart %(process)s" % env)


@task
@log_call
def restart_memcached():
    """ Restarts the Memcached server. """
    sudo("service memcached restart")


@task
@log_call
def reload_nginx():
    """ Restarts the nginx process. """
    check_nginx(log=False)
    nginx("reload")


@task
@log_call
def check_nginx():
    """ Checks the Nginx config. """
    with settings(hide('warnings', 'running', 'stdout', 'stderr')):
        result = sudo("service nginx configtest", quiet=True, show=False)

        if result.failed:
            error("Aborting! Nginx failed the configuration test!\n%s" %
                  result)


@task
@log_call
def restart_tomcat():
    """ Restarts the nginx process. """
    sudo("service tomcat6 restart")


@task(alias='re')
@log_call
def restart(*services):
    """ Restarts the given service. """
    options = {
        'celery': restart_celery,
        'django': restart_django,
        'memcached': restart_memcached,
        'nginx': reload_nginx,
        'tomcat': restart_tomcat,
    }

    funcs = []

    for service in services:
        func = options.get(service.lower())
        if not func:
            raise Exception("Unrecognized service %s", service)
        funcs.append(func)

    for func in funcs:
        func(log=False)


@task
@log_call
def rsync(remote_path, local_path, options="-avzr --progress"):
    """ Runs rsync with the remote path as the source, and the local path
    as the destination.
    """
    local("rsync %s %s:%s %s" % (
        options,
        env.host_string,
        remote_path,
        local_path,
    ))


@task
@log_call
def timestamp(_format='%Y-%m-%d %H:%M:%S', quiet=False):
    border = yellow
    sep = ' ⌚ '
    char = '•'
    side = border(char)

    stamp = run('date +"%s"' % _format, show=False, quiet=True)

    if not quiet:
        line = border(char * (
            len(' '.join([env.host_string, sep, stamp])) + 2))

        output = ' '.join([
            side,
            green(stamp, bold=True),
            blue(sep, bold=True),
            white(env.host_string, bold=True),
            side,
        ])

        puts('\n' + indent([line, output, line], spaces=4) + '\n',
             show_prefix=False)

    return stamp


@task
@log_call
def tailgun(log_file):
    """ Tails a given log file. If the given path is relative, the path is
    prepended with env.log.
    """
    if not log_file.startswith('/'):
        log_file = os.path.join(env.log, log_file)

    timestamp(log=False)

    with settings(output_prefix=False):
        sudo('true', quiet=True, show=False)
        sudo('tail -f %s' % log_file)

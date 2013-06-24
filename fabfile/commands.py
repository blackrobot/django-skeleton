import os

from fabric.api import cd, env, task

from .utils import log_call, run, sudo


__all__ = ['get_binary', 'chmod', 'chown', 'python', 'git', 'pip', 'nginx',
           'supervisor']


def get_binary(name):
    """ This returns the path of a binary file called `name` in the virtual
    environment.
    """
    return os.path.join(env.venv, 'bin', name)


def _get_abs_path(path):
    """ Returns the path prepended with the base_dir if it does not start with
    a '/'.
    """
    return os.path.join(env.base, path) if not path.startswith('/') else path


def _get_flags(flags):
    """ Returns flags prefixed with a '-' if it's not there. """
    return (flags and not flags.startswith('-') and '-%s' % flags) or flags


def _prep_cmd(*args):
    """ Takes a list of strings, and returns them joined and stripped. """
    return ' '.join(args).strip()


@task
@log_call
def chmod(cmd="", flags="", perms="", path=""):
    """ Given the flags, permissions, and path this will run chmod. If the
    path doesn't have a leading '/', it will be prepended with the base_dir.
    """
    if not cmd:
        cmd = _prep_cmd(_get_flags(flags), perms, _get_abs_path(path))
    sudo("chmod %s" % cmd)


@task
@log_call
def chown(cmd="", flags="", user="", group="", path=""):
    """ Given the flags, user, group, and path this will run chown. If the
    path doesn't have a leading '/' it will be prepended with the base_dir.
    """
    if not cmd:
        cmd = _prep_cmd(
            _get_flags(flags),
            ("%s:%s" % (user, group)) if user and group else user,
            _get_abs_path(path),
        )
    sudo("chown %s" % cmd)


@task
def python(args):
    """ Runs a command with the environment's python binary. """
    return run("%s %s" % (get_binary('python'), args))


@task
def git(args):
    """ Run a git command on the remote server. """
    with cd(env.app):
        return run("git %s" % args)


@task
def pip(args, execute=True):
    """ Runs pip in the environment with the given command. """
    command = "%s %s" % (get_binary('pip'), args)
    if execute:
        return run(command)
    return command


@task
def nginx(args):
    """ Runs an Nginx command with the given args. """
    return sudo("service nginx %s" % args)


@task
def supervisor(args):
    """ Runs a supervisor command with the given args. """
    return sudo("supervisorctl %s" % args)

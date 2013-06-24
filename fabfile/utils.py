from pprint import pformat

from functools import wraps

from fabric.api import env, hide, task, run as _run, sudo as _sudo
from fabric.colors import blue, green, red, white, yellow
from fabric.utils import abort, indent, puts, warn


LINE_CHAR = '-'
PREP_TEXT = lambda text: white(text, bold=True)


_join = lambda l: PREP_TEXT(', ').join(l)


def make_tmpl(title, subtext):
    return '\n{}\n{}\n'.format(indent(title + ":"), indent(subtext, spaces=8))


LOG_TMPL = make_tmpl("Python", "%s{}%s{}".format(*(PREP_TEXT(c)for c in '()')))
PRINT_TMPL = make_tmpl("Shell", "%s %s")


def banner(template, *args):
    """ Runs puts with some defaults. """
    puts(template % args, show_prefix=False)


def log_call(func):
    @wraps(func)
    def logged(*args, **kwargs):
        if 'log' in kwargs and not kwargs['log']:
            kwargs.pop('log')
            return func(*args, **kwargs)
        name = PREP_TEXT(func.__name__)
        _vars = []
        for val in args:
            _vars.append(green(pformat(val), bold=True))
        for key, val in kwargs.items():
            _vars.append(blue(key, bold=True) + blue('=') +
                         green(pformat(val), bold=True))
        banner(LOG_TMPL, name, _join(_vars))
        return func(*args, **kwargs)
    return logged


def print_command(command, sudo=False):
    """ Prints the given command, a string, with some fancy formatting. """
    char = blue('#' if sudo else '$', bold=True)
    banner(PRINT_TMPL, char, yellow(command, bold=True))


def error(message):
    """ Outputs the error message, and aborts the operation. """
    abort(red('\n' + indent(message), bold=True))


def success(message):
    """ Outputs the success message. """
    puts(green(indent(message), bold=True))


def warning(message):
    """ Outputs the warning message. """
    warn(yellow(message, bold=True))


@task
def run(command, quiet=False, show=True):
    """ Runs a shell command on the remote server. """
    if show:
        print_command(command)

    with hide("running"):
        if 'deploy_user' in env:
            # If a deploy_user is specified, run as that user
            return _sudo(command, quiet=quiet, user=env.deploy_user)
        return _run(command, quiet=quiet)


@task
def sudo(command, quiet=False, show=True):
    """ Runs a command as sudo. """
    if show:
        print_command(command, sudo=True)

    with hide("running"):
        return _sudo(command, quiet=quiet)

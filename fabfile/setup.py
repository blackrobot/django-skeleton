import os

from fabric.api import env, task
from fabric.contrib.files import exists

from .commands import git
from .utils import log_call, run


__all__ = ['checkout', 'virtualenv']


@task
@log_call
def checkout():
    """ This will checkout the project into the env.app directory. """
    if not exists(os.path.join(env.app, 'fabfile')):
        run("git clone %(repo)s %(app)s" % env)
        return git("checkout %(branch)s" % env)


@task
@log_call
def virtualenv():
    """ This will create the virtual environment, and symlink it. """
    workon_home = run("echo $WORKON_HOME", quiet=True, show=False).strip()

    if not workon_home:
        workon_home = os.path.join('~', '.virtualenvs')

    run(' && '.join(["export WORKON_HOME=%s" % workon_home,
                     "source /usr/bin/virtualenvwrapper.sh",
                     "mkvirtualenv %s" % (env.process or env.site_url)]))

    # Symlink it into the project
    run("ln -s %s %s" % (os.path.join(workon_home, env.site_url), env.venv))

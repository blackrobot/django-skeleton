from fabric.api import env, local


__all__ = ['configure']


def configure():
    """ Sets up the environment for vagrant. """
    env.disable_known_hosts = True

    # Collect the connection information from the vagrant-ssh command and
    # create a dictionary from it.
    out = local('vagrant ssh-config', capture=True).splitlines()[1:]
    conf = {k: v for k, v in (l.strip().split(' ', 2) for l in out)}

    env.hosts = ['%(User)s@%(HostName)s:%(Port)s' % conf]
    env.key_filename = conf['IdentityFile'].strip('"')

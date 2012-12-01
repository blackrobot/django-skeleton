""" This allows you to run `$ python manage.py runserver` without specifying
the settings. On different environments, be sure to add their own
source/settings/<env>.py to the repository, and symlink that file to
source/settings/local.py
"""
try:
    from source.settings.local import *
except ImportError:
    raise ImportError("Cannot find a local settings file. Have you set one "
                      "up, or symlinked one to source/settings/local.py?")

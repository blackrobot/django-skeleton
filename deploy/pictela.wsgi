import os
import sys
import site

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['PYTHON_EGG_CACHE'] = '/var/www/django/.python-eggs'

site.addsitedir('/var/www/django/pictela/env/lib/python2.6/site-packages')
sys.path.append('/var/www/django/pictela/src')
 
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

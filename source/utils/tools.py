import os

from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import directory_index
from django.shortcuts import redirect
from django.views.generic.simple import direct_to_template



def html_design_view(*args, **kwargs):
    """ This will load design templates from the "html" directory in your
    templates folder. It's only turned on if DEBUG is True. It will also
    show indexes if you leave off the filename and extension.
    """
    path = kwargs['path']

    # The path is a directory
    if path.endswith('/'):
        directory = os.path.join(settings.HTML_DESIGN_ROOT, path)
        return directory_index(path.rstrip('/'), directory)

    # Missing a trailing slash
    elif '.' not in path.split('/')[-1].find('.'):
        return redirect('/%s/' % path)

    # Render the template
    kwargs['template'] = path
    return direct_to_template(*args, **kwargs)


def html_design_urlpatterns():
    re = r"^%s/(?P<path>.*)$" % settings.HTML_DESIGN_NAMESPACE
    return patterns('', url(re, html_design_view))


def local_serve_urlpatterns():
    re = r"^%s(?P<path>.*)$" % settings.MEDIA_URL.lstrip('/')
    options = {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}

    return patterns('django.views.static',
        url(re, 'serve', options),
    ) + staticfiles_urlpatterns()

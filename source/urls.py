import os

from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import redirect
from django.views.static import directory_index
from django.views.generic.simple import direct_to_template


admin.autodiscover()

urlpatterns = patterns('',
    # Django Admin
    (r"^%s/" % settings.ADMIN_NAMESPACE, include(admin.site.urls)),

    # Now in a template, you can access: {% url "some_namespace:url_name" %}
    #  url(r"^name/$", inclue('app.name.urls', namespace="some_namespace")),
    #  url(r"^(?P<slug>[-\w]+)/$", 'some_view', name="url_name"),
)

if getattr(settings, "DEBUG", False):
    """ This will load design templates from the "html" directory in your
    templates folder. It's only turned on if DEBUG is True. It will also
    show indexes if you leave off the filename and extension.
    """
    def h(*args, **kwargs):
        t = "%s/%s" % (kwargs['base'], kwargs['template'])
        if t.endswith('/'):
            template_path = os.path.join(settings.PROJECT_PATH, "templates", t)
            return directory_index(t.rstrip('/'), template_path)
        elif t.split('/')[-1].find('.') == -1:
            return redirect("/%s/" % t)
        kwargs['template'] = t
        return direct_to_template(*args, **kwargs)

    urlpatterns = patterns('',
        url(r"^(?P<base>html)/(?P<template>.*)$", h),
    ) + urlpatterns

if getattr(settings, "LOCAL_SERVE", False):
    urlpatterns = patterns('django.views.static',
        url(r"^%s(?P<path>.*)$" % settings.MEDIA_URL.lstrip('/'), "serve", {
            'document_root': settings.MEDIA_ROOT, 'show_indexes': True,
        }),
    ) + staticfiles_urlpatterns() + urlpatterns

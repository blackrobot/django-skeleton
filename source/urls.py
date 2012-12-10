from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

from source.utils.tools import html_design_urlpatterns, local_serve_urlpatterns


admin.autodiscover()

urlpatterns = patterns('',
    # Django Admin
    url(r"^%s/" % settings.ADMIN_NAMESPACE, include(admin.site.urls)),

    # Now in a template, you can: reverse("some_namespace:url_name")
    #  url(r"^name/$", inclue('app.name.urls', namespace="some_namespace")),
    #  url(r"^(?P<slug>[-\w]+)/$", 'some_view', name="url_name"),
)

if getattr(settings, "DEBUG", False):
    urlpatterns = html_design_urlpatterns() + urlpatterns

if getattr(settings, "LOCAL_SERVE", False):
    urlpatterns = local_serve_urlpatterns() + urlpatterns

# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.urls import include, path  # For django versions from 2.0 and up
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.views import defaults as default_views

from business.views import entry

urlpatterns = [
    url(settings.ADMIN_URL, admin.site.urls),
    url(r'', include('business.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^$', entry, name='home'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception("Permission Denied")}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception("Page not Found")}),
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception("Bad Request!")}),
        url(r'^500/$', default_views.server_error),
    ]
    import debug_toolbar

    urlpatterns += [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ]

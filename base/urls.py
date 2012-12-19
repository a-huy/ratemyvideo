from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
from django.views.defaults import server_error

urlpatterns = patterns('',
    url(r'^accounts/', include('accounts.api.urls')),
    url(r'^videos/', include('videos.api.urls')),
)

urlpatterns += patterns('base.views',
    url(r'^get/$', 'download_extension', name='download_extension'),
)


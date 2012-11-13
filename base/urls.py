from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^accounts/', include('accounts.api.urls')),
    (r'^videos/', include('videos.api.urls')),
    (r'^get/$', 'download_extension', name='download_extension'),
)

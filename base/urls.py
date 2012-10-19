from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^accounts/', include('accounts.api.urls')),
    (r'^videos/', include('videos.api.urls')),
)

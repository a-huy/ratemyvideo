import os
import base.views

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.http import HttpResponse

handler500 = base.views.custom_500

urlpatterns = patterns('',
    url(r'^$', include('homepage.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^legal/', include('homepage.urls')),
    url(r'^videos/', include('videos.urls')),
    url(r'^login/', include('accounts.urls')),
    url(r'^rmvadmin/', include('rmvadmin.urls')),
    url(r'^api/', include('base.urls')),
    url(r'^content/(.*)$', 'django.views.static.serve', 
        {'document_root': os.path.join(settings.PROJECT_PATH, 'content')}),
    url(r'^extension/', include('base.urls')),
    url(r'^robots\.txt$', 
        lambda r: HttpResponse('User-agent: *\nDisallow: /', mimetype='text/plain')),
)


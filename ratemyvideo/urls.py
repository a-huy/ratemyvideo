import os

from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('homepage.urls')),
    url(r'^videos/', include('videos.urls')),
    url(r'^login/', include('accounts.urls')),
    url(r'^rmvadmin/', include('rmvadmin.urls')),
    url(r'^api/', include('base.urls')),
    url(r'^content/(.*)$', 'django.views.static.serve', 
        {'document_root': os.path.join(settings.PROJECT_PATH, 'content')}),
    url(r'^extension/', include('base.urls')),
    
    # Examples:
    # url(r'^$', 'ratemyvideo.views.home', name='home'),
    # url(r'^ratemyvideo/', include('ratemyvideo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


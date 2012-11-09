from django.conf.urls import patterns, include, url

urlpatterns = patterns('rmvadmin.views',
    url(r'^$', 'home', name='home'),
    url(r'^login/$', 'rmv_login', name='rmv_login'),
    url(r'^logout/$', 'rmv_logout', name='rmv_logout'),
    url(r'^list_videos/$', 'list_videos', name='list_videos'),
    url(r'^add_video/$', 'add_video', name='add_video'),
    url(r'^edit_whitelist/$', 'edit_whitelist', name='edit_whitelist'),
)

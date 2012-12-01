from django.conf.urls import patterns, include, url

urlpatterns = patterns('rmvadmin.views',
    url(r'^$', 'home', name='rmvhome'),
    url(r'^login/$', 'rmv_login', name='rmv_login'),
    url(r'^logout/$', 'rmv_logout', name='rmv_logout'),
    url(r'^list_users/$', 'list_users', name='list_users'),
    url(r'^list_videos/$', 'list_videos', name='list_videos'),
    url(r'^add_video/$', 'add_video', name='add_video'),
    url(r'^whitelist/$', 'whitelist', name='whitelist'),
    url(r'^invites/$', 'invites', name='invites'),
    url(r'^user/(?P<fb_id>[0-9]+)/$', 'user_info', name='user_info'),
)

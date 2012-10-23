from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.api.user',
    (r'^user/$', 'UserCreateApi'),
    (r'^user/(?P<fb_id>[0-9]+)/$', 'UserUpdateApi'),
)

urlpatterns += patterns('accounts.api.queue',
    (r'^queue/(?P<fb_id>[0-9]+)/$', 'QueueApi'),
)

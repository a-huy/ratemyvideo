from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.api.user',
    (r'^user/$', 'UserCreateApi'),
    (r'^user/(?P<fb_id>[0-9]+)/$', 'UserUpdateApi'),
)

urlpatterns += patterns('accounts.api.queue',
    (r'^queue/(?P<fb_id>[0-9]+)/$', 'QueueApi'),
)

urlpatterns += patterns('accounts.api.session',
    (r'^session/$', 'SessionApi'),
)

urlpatterns += patterns('accounts.api.rating',
    (r'^ratings/(?P<fb_id>[0-9]+)/$', 'RatingHistoryApi'),
)

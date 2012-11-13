from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.api.user',
    url(r'^user/(?P<fb_id>[0-9]+)/$', 'UserUpdateApi'),
)

urlpatterns += patterns('accounts.api.queue',
    url(r'^queue/(?P<fb_id>[0-9]+)/$', 'QueueApi'),
)

urlpatterns += patterns('accounts.api.session',
    url(r'^session/$', 'SessionApi'),
)

urlpatterns += patterns('accounts.api.rating',
    url(r'^ratings/(?P<fb_id>[0-9]+)/$', 'RatingHistoryApi'),
)

urlpatterns += patterns('accounts.api.invite',
    url(r'^request/invite/$', 'InviteApi'),
)

urlpatterns += patterns('accounts.api.whitelist',
    url(r'^whitelist/$', 'WhiteListCreateApi'),
)


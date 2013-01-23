from django.conf.urls import patterns, include, url

urlpatterns = patterns('accounts.views',
    url(r'^$', 'login_page', name='login_page'),
    url(r'^profile/(?P<fb_id>[0-9]+)/$', 'profile', name='profile'),
    url(r'^channel/$', 'channel', name='channel'),
    url(r'^invite_required/$', 'invite_required', name='invite_required'),
)

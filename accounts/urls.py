from django.conf.urls import patterns, include, url

urlpatterns = patterns('accounts.views',
    url(r'^$', 'login_page', name='login_page'),
    url(r'^channel/$', 'channel', name='channel'),
)

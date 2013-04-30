from django.conf.urls import patterns, include, url

urlpatterns = patterns('homepage.views',
    url(r'^$', 'homepage', name='homepage'),
    url(r'^privacy-policy/$', 'privacy_policy', name='privacy_policy'),
    url(r'^terms-of-service/$', 'terms_of_service', name='terms_of_service'),
    url(r'^faq/$', 'faq', name='faq'),
    url(r'^signup/$', 'signup', name='signup'),
    url(r'^about/$', 'about', name='about'),
    url(r'^comment/$', 'comment', name='comment'),
)

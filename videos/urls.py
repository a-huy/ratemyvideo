from django.conf.urls import patterns, include, url

urlpatterns = patterns('videos.views',
    url(r'^(?P<video_id>[a-zA-z0-9]{11})/$', 'video_page', name='video_page'),
)

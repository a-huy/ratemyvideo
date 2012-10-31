from django.conf.urls.defaults import *

urlpatterns = patterns('videos.api.rating',
    (r'^rating/$', 'RatingCreateApi'),
    (r'^vote/$', 'VoteCreateApi'),
)


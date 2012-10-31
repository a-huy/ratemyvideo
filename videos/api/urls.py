from django.conf.urls.defaults import *

urlpatterns = patterns('videos.api.rating',
    (r'^rating/$', 'RatingCreateApi'),
)

urlpatterns += patterns('videos.api.vote',
    (r'^vote/$', 'VoteCreateApi'),
)


from django.conf.urls.defaults import *

urlpatterns = patterns('videos.api.rating',
    (r'^rating/$', 'RatingCreateApi'),
)

urlpatterns += patterns('videos.api.vote',
    (r'^vote/$', 'VoteCreateApi'),
)

urlpatterns += patterns('videos.api.video',
    (r'^video/$', 'VideoCreateApi'),
)

urlpatterns += patterns('videos.api.comment',
    (r'^comment/$', 'CommentCreateApi'),
)

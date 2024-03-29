# Not to be confused with videos/api/rating.py,
# this API is for a user's rating history

import datetime
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.conf import settings
#from django.core.cache import cache

import base.api.base as base
#import base.cache_keys as keys
import videos.models as videos_models
import accounts.models as accounts_models
from base.contrib import whitelisted

class RatingHistoryApi(base.RestView):

    model = videos_models.Rating

    def GET(self, request, fb_id, *args, **kwargs):
        if not whitelisted(fb_id):
            return HttpResponseForbidden('User has not been authenticated')
        try:
            user = accounts_models.User.active.get(fb_id=fb_id)
        except accounts_models.User.DoesNotExist:
            return HttpResponseBadRequest('Invalid FB ID')

#        history_key = keys.ACC_USER_HISTORY % user.fb_id
#        ratings_list = cache.get(history_key)
#        if not ratings_list:
        ratings = videos_models.Rating.objects.filter(user_id=user.id)
        ratings = ratings.order_by('-created_date')[:settings.DEFAULT_RATING_LIST_LIMIT]
        videos = [rating.video for rating in ratings]

        ratings_list = []
        for rating in ratings:
            video = filter(lambda x:rating.video_id == x.id, videos)[0]
            ratings_list.append({
                'date': {
                    'year':rating.created_date.year,
                    'month':rating.created_date.month,
                    'day':rating.created_date.day,
                    'hour':rating.created_date.hour,
                    'minute':rating.created_date.minute,
                    'second':rating.created_date.second,
                    'microsecond':rating.created_date.microsecond
                },
                'rating': rating.rating,
                'title': video.title,
                'reward': video.reward,
                'yt_id': video.yt_id
            })
#        cache.set(history_key, ratings_list)

        data = { 'result': ratings_list }
        return base.APIResponse(data)

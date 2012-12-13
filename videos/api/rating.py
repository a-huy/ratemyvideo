import datetime

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.utils.timezone import now
from django.core.cache import cache

import base.api.base as base
import base.cache_keys as keys
import accounts.models as accounts_models
import videos.models as videos_models
import videos.forms as videos_forms
from base.contrib import timedelta_to_seconds, extract_addr

class RatingCreateApi(base.RestView):

    model = videos_models.Rating

    def POST(self, request, *args, **kwargs):
        if 'fb_id' not in request.POST or not request.POST['fb_id']:
            return HttpResponseBadRequest('A Facebook ID is required')
        if 'yt_id' not in request.POST or not request.POST['yt_id']:
            return HttpResponseBadRequest('A YouTube Video ID is required')
        if 'rating' not in request.POST or not request.POST['rating']:
            return HttpResponseBadRequest('A numeric rating is required')
        fields = request.POST
        try:
            account = accounts_models.User.active.get(fb_id=fields['fb_id'])
            video = videos_models.Video.active.get(yt_id=fields['yt_id'])
            queue_entry = videos_models.Queue.active.get(user_id=account.id, video_id=video.id) ###
            rating = videos_models.Rating.active.get(user_id=account.id, video_id=video.id)
            return HttpResponseBadRequest('Users cannot rate a video more than once')
        except accounts_models.User.DoesNotExist:
            return HttpResponseBadRequest('Invalid Facebook ID')
        except videos_models.Video.DoesNotExist:
            return HttpResponseBadRequest('Invalid YouTube Video ID')
        except videos_models.Queue.DoesNotExist: ###
            return HttpResponseBadRequest('User is not authorized to rate that video') ###
        except videos_models.Rating.DoesNotExist:
            pass

        # Uncomment to prevent batch ratings (rating quickly in a small period of time)
#        time_since_last_rating = datetime.timedelta(999999999)
#        user_ratings = videos_models.Rating.active.filter(user_id=account.id).order_by('-created_date')
#        if len(user_ratings) != 0:
#            time_since_last_rating = now() - user_ratings[0].created_date
#        if timedelta_to_seconds(time_since_last_rating) < video.duration:
#            return HttpResponseBadRequest('Please watch the entire video before rating.')

        new_rating = videos_models.Rating()
        new_rating.video_id = video.id
        new_rating.user_id = account.id
        new_rating.rating = fields['rating']
        new_rating.source_ip = extract_addr(request) or '0.0.0.0'
        new_rating.save()
        account.rated += 1
        account.earned += video.reward
        account.balance += video.reward
        account.save()
        queue_entry.delete() ###

        # Invalidate user queue and rating history
        cache.delete(keys.ACC_USER_QUEUE % account.fb_id)
#        cache.delete(keys.ACC_USER_HISTORY % account.fb_id)

        return base.APIResponse(new_rating.to_json())

class RatingUpdateApi(base.RestView):

    model = videos_models.Rating

    def GET(self, request, fb_id, *args, **kwargs):
        return HttpResponse()


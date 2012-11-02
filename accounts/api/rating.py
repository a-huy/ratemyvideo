import datetime
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest

import base.api.base as base
import videos.models as videos_models
import accounts.models as accounts_models

class RatingHistoryApi(base.RestView):

    model = videos_models.Rating
    
    def GET(self, request, fb_id, *args, **kwargs):
        
        try:
            user = accounts_models.User.objects.get(fb_id=fb_id)
        except accounts_models.User.DoesNotExist:
            return HttpResponseBadRequest('Invalid FB ID')
        ratings = videos_models.Rating.objects.filter(user_id=user.id).order_by('created_date')
        videos = videos_models.Video.objects.filter(id__in=[r.video_id for r in ratings])
        
        ratings_list = []
        for rating in ratings:
            video = filter(lambda x:rating.video_id == x.id, videos)[0]
            ratings_list.append({
                'date': rating.created_date,
                'rating': rating.rating,
                'title': video.title,
                'reward': video.reward
            })
        data = { 'result': ratings_list }
        return base.APIResponse(data)

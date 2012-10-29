from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest

import base.api.base as base
import accounts.models as accounts_models
import videos.models as videos_models
import videos.forms as videos_forms

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
            account = accounts_models.User.objects.get(fb_id=fields['fb_id'])
            video = videos_models.Video.objects.get(yt_id=fields['yt_id'])
            rating = videos_models.Rating.objects.get(user_id=account.id, 
                                                      video_id=video.id)
            return HttpResponseBadRequest('Users cannot rate a video more than once')
        except accounts_models.User.DoesNotExist:
            return HttpResponseBadRequest('Invalid Facebook ID')
        except videos_models.Video.DoesNotExist:
            return HttpResponseBadRequest('Invalid YouTube Video ID')
        except videos_models.Rating.DoesNotExist:
            new_rating = videos_models.Rating()
            new_rating.video_id = video.id
            new_rating.user_id = account.id
            new_rating.rating = fields['rating']
            new_rating.save()
        return base.APIResponse(new_rating.to_json())

class RatingUpdateApi(base.RestView):
    
    model = videos_models.Rating
    
    def GET(self, request, fb_id, *args, **kwargs):
        return HttpResponse()
        

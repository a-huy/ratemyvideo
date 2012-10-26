from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest

import base.api.base as base
import accounts.models as accounts_models
import accounts.forms as accounts_forms
import videos.models as videos_models

class QueueApi(base.RestView):
    
    def GET(self, request, fb_id, *args, **kwargs):
        #try:
        #    user = accounts_models.User.get(fb_id=user_id)
        #except accounts_models.User.DoesNotExist:
        #gh    return HttpResponseBadRequest('User ID invalid')
        
        uid = accounts_models.User.objects.get(fb_id=fb_id)
        vid_ids = [v.video_id for v in 
                   videos_models.Rating.objects.filter(user_id=uid)]
        videos = list(videos_models.Video.objects.all())
        videos = filter(lambda x: x.id not in vid_ids, videos)
        
        data = {
            'vid_ids': [vid.yt_id for vid in videos],
            'host': request.get_host()
        }
        
        return base.APIResponse(data)


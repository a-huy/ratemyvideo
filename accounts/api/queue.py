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
        
        videos = videos_models.Video.objects.all()
        
        data = {
            'vid_ids': [vid.yt_id for vid in videos]
        }
        
        return base.APIResponse(data)


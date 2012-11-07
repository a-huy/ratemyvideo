from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest

import base.api.base as base
import accounts.models as accounts_models
import accounts.forms as accounts_forms
import videos.models as videos_models

class QueueApi(base.RestView):
    
    def GET(self, request, fb_id, *args, **kwargs):

        try:
            uid = accounts_models.User.objects.get(fb_id=fb_id)
        except accounts_models.User.DoesNotExist:
            return HttpResponseBadRequest('Invalid fb_id')
        vid_ids = [v.video_id for v in 
                   videos_models.Rating.objects.filter(user_id=uid)]
        videos = list(videos_models.Video.objects.all())
        videos = filter(lambda x: x.id not in vid_ids, videos)
        
        vids = []
        for vid in videos[:10]:
            vids.append({
                'yt_id': vid.yt_id, 
                'reward': vid.reward, 
                'title': vid.title
            })
        
        data = {
            'vids': vids,
            'host': request.get_host()
        }
        
        return base.APIResponse(data)


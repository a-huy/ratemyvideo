from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, \
    HttpResponseForbidden
#from django.core.cache import cache

import base.api.base as base
import accounts.models as accounts_models
import accounts.forms as accounts_forms
import videos.models as videos_models
from base.contrib import whitelisted
#import base.cache_keys as keys

class QueueApi(base.RestView):

    def GET(self, request, fb_id, *args, **kwargs):

        try:
            uid = accounts_models.User.active.get(fb_id=fb_id)
        except accounts_models.User.DoesNotExist:
            return HttpResponseBadRequest('Invalid fb_id')
        if not whitelisted(fb_id):
            return HttpResponseForbidden('User has not been authenticated')

#        queue_key = keys.ACC_USER_QUEUE % uid.fb_id
#        vids = cache.get(queue_key)
#        if not vids:
        vid_ids = [v.video_id for v in videos_models.Queue.objects.filter(user_id=uid)]
        videos = videos_models.Video.active.filter(id__in=vid_ids)

        vids = []
        for vid in videos:
            vids.append({
                'yt_id': vid.yt_id,
                'reward': vid.reward,
                'title': vid.title
            })
#        cache.set(queue_key, vids)

        data = {
            'vids': vids,
            'host': request.get_host()
        }

        return base.APIResponse(data)


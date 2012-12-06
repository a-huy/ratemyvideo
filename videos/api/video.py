from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.utils.encoding import smart_text

import base.api.base as api_base
import base.contrib
import videos.models as videos_models
import videos.lib.video as video_lib

class VideoCreateApi(api_base.RestView):

    model = videos_models.Video

    def POST(self, request, *args, **kwargs):
        if 'yt_id' not in request.POST or not request.POST['yt_id']:
            return HttpResponseBadRequest('A YouTube Video ID is required')
        if not base.contrib.valid_yt_id(request.POST['yt_id']):
            return HttpResponseBadRequest('YouTube ID is not in a correct format ' +
                '(11 characters, only letters, numbers, dashes, and underscores allowed)')
        if 'reward' not in request.POST or not request.POST['reward']:
            return HttpResponseBadRequest('A reward is required')
        yt_id = request.POST['yt_id']
        if 'tags' in request.POST and request.POST['tags']: tags = request.POST['tags']
        else: tags = ''

        # Validate reward
        try:
            reward = float(request.POST['reward'])
            if reward > 1: return HttpResponseBadRequest('Reward amount must not exceed $1')
        except ValueError: return HttpResponseBadRequest('Invalid reward amount')

        # Check if video already exists
        try:
            video = videos_models.Video.active.get(yt_id=yt_id)
            return HttpResponseBadRequest('Video is already being rated')
        except videos_models.Video.DoesNotExist:
            pass

        gdata_obj = video_lib.get_info_from_yt_id(yt_id)
        duration = gdata_obj.media.duration.seconds if gdata_obj else 0

        title = request.POST.get('title', None)
        if not title:
            title = gdata_obj.title.text if gdata_obj else 'Unknown'
        if not title: return HttpResponseBadRequest('Invalid YouTube ID')

        new_video = videos_models.Video()
        new_video.yt_id = yt_id
        new_video.reward = reward
        new_video.title = smart_text(title)
        new_video.duration = duration
        new_video.tags = tags
        new_video.save()
        return api_base.APIResponse('new video added')

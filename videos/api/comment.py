from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest

import base.api.base as base
import accounts.models as accounts_models
import videos.models as videos_models
from base.contrib import extract_addr

class CommentCreateApi(base.RestView):

    model = videos_models.Comment

    def POST(self, request, *args, **kwargs):
        if 'fb_id' not in request.POST or not request.POST['fb_id']:
            return HttpResponseBadRequest('A Facebook ID is required')
        if 'yt_id' not in request.POST or not request.POST['yt_id']:
            return HttpResponseBadRequest('A YouTube Video ID is required')
        if 'text' not in request.POST:
            return HttpResponseBadRequest('A comment is required')
        fields = request.POST

        try:
            account = accounts_models.User.active.get(fb_id=fields['fb_id'])
            video = videos_models.Video.active.get(yt_id=fields['yt_id'])
        except accounts_models.User.DoesNotExist:
            return HttpResponseBadRequest('Invalid Facebook ID')
        except videos_models.Video.DoesNotExist:
            return HttpResponseBadRequest('Invalid YouTube Video ID')
        new_comment = videos_models.Comment()
        new_comment.video = video
        new_comment.user = account
        new_comment.text = fields['text']
        new_comment.source_ip = extract_addr(request) or '0.0.0.0'
        new_comment.save()
        account.commented += 1
        account.karma += 1
        account.save()
        return base.APIResponse('commenting successful')

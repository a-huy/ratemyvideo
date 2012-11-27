from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest

import base.api.base as base
import accounts.models as accounts_models
import videos.models as videos_models
import videos.forms as videos_forms
from base.contrib import extract_addr

class VoteCreateApi(base.RestView):

    model = videos_models.Vote
    
    def POST(self, request, *args, **kwargs):
        if 'fb_id' not in request.POST or not request.POST['fb_id']:
            return HttpResponseBadRequest('A Facebook ID is required')
        if 'yt_id' not in request.POST or not request.POST['yt_id']:
            return HttpResponseBadRequest('A YouTube Video ID is required')
        if 'like' not in request.POST or not request.POST['like']:
            return HttpResponseBadRequest('A like status is required')
        fields = request.POST
        try:
            account = accounts_models.User.objects.get(fb_id=fields['fb_id'])
            video = videos_models.Video.objects.get(yt_id=fields['yt_id'])
            vote = videos_models.Vote.objects.get(user_id=account.id, 
                                                  video_id=video.id)
            return HttpResponseBadRequest('You cannot vote on a video more than once.')
        except accounts_models.User.DoesNotExist:
            return HttpResponseBadRequest('Invalid Facebook ID')
        except videos_models.Video.DoesNotExist:
            return HttpResponseBadRequest('Invalid YouTube Video ID')
        except videos_models.Vote.DoesNotExist:
            new_vote = videos_models.Vote()
            new_vote.video_id = video.id
            new_vote.user_id = account.id
            new_vote.like = True if fields['like'] == 'True' else False
            new_vote.source_ip = extract_addr(request) or '0.0.0.0'
            new_vote.save()
            account.liked += 1 if fields['like'] == 'True' else 0
            account.karma += 1
            account.save()
        return base.APIResponse('voting successful');


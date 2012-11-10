import hashlib

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.conf import settings
from django.contrib.auth.decorators import login_required

import base.api.base as base
import accounts.models as accounts_models
import accounts.forms as accounts_forms


class WhiteListCreateApi(base.RestView):

    model = accounts_models.UserWhitelist

    @login_required
    def POST(self, request, *args, **kwargs):
        if 'fb_id' not in request.POST or not request.POST['fb_id']:
            return HttpResponseBadRequest('A whitelist seed is required')
        try:
            inv_req = accounts_models.InviteRequest.active.get(fb_id=request.POST['fb_id'])
        except accounts_models.InviteRequest.DoesNotExist:
            return HttpResponseBadRequest('Invite request could not be found')

        hash_key = hashlib.sha512('rmv:whitelist:' + inv_req.fb_id).hexdigest()
        new_entry = accounts_models.UserWhitelist({'key':hash_key})
        new_entry.save()

        return HttpResponse('The whitelist has been updated!')

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import redirect
from django.conf import settings
import urllib
import cgi
import json

import base.api.base as base
import accounts.models as accounts_models
import accounts.forms as accounts_forms
import accounts.lib.invite as invite_lib

class InviteApi(base.RestView):

    model = accounts_models.InviteRequest

    def GET(self, request, *args, **kwargs):
        args = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': settings.DOMAIN + 'api/accounts/request/invite/'
        }
        if 'code' not in request.GET or not request.GET['code']:
            args['scope'] = 'email,user_birthday,user_location,read_stream'
            return redirect('https://graph.facebook.com/oauth/authorize?' +
                urllib.urlencode(args))

        args['code'] = request.GET.get('code')
        user = invite_lib.get_user_data(args)
        user['reason'] = request.GET.get('state', '')
        elig_result = invite_lib.account_is_eligible(user)
        if not elig_result[0]: return HttpResponseBadRequest(elig_result[1])
        try:
            invite_req = accounts_models.InviteRequest.objects.get(fb_id=user['fb_id'])
            return HttpResponseBadRequest('You have already submitted an invite request.')
        except accounts_models.InviteRequest.DoesNotExist:
            pass
        invite_lib.create_request(user)
        return HttpResponse('Request received!')

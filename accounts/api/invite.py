from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import redirect
from django.conf import settings
import urllib
import json

import base.api.base as base
from base.contrib import backend_email, send_email
from base.views import message_response
import accounts.models as accounts_models
import accounts.forms as accounts_forms
import accounts.lib.invite as invite_lib

class InviteApi(base.RestView):

    model = accounts_models.InviteRequest

    # This is used to create invites because Facebook sends a GET request
    # to the redirect page
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
        send_email('confirm_invite', 'anguyenhuy@gmail.com', request.META['REMOTE_ADDR'])
        user = invite_lib.get_user_data(args, request)
        user['reason'] = request.GET.get('state', '')
        elig_result = invite_lib.account_is_eligible(user)
        if not elig_result[0]: return message_response(request, 400, elig_result[1])
        # Users cannot submit multiple pending requests
        try:
            invite_req = accounts_models.InviteRequest.active.get(fb_id=user['fb_id'])
            return message_response(request, 400,
                'You have already submitted an invite request.')
#            return HttpResponseBadRequest('You have already submitted an invite request.')
        except accounts_models.InviteRequest.DoesNotExist:
            pass
        # Users cannot submit a request if they are already using the service
        try:
            user = accounts_models.User.active.get(fb_id=user['fb_id'])
            return message_response(request, 400, 'You already have access to this service!')
#            return HttpResponseBadRequest('You already have access to this service!')
        except accounts_models.User.DoesNotExist:
            pass
        invite_lib.create_request(user)
        email_args = [user['fb_id'], user['real_name'], user['email'], user['location'],
            user['age'], user['gender'], user['reason'], user['fb_id'], settings.DOMAIN]
        send_email('confirm_invite', user['email'], [user['real_name']])
        backend_email('new_invite_request', 'admins', email_args)
        return message_response(request, 200, 'Request received!')
#        return HttpResponse('Request received!')

    def DELETE(self, request, *args, **kwargs):
        if 'fb_id' not in request.POST or not request.POST['fb_id']:
            return HttpResponseBadRequest('Invalid Facebook ID given')
        try:
            inv_req = accounts_models.InviteRequest.active.get(fb_id=request.POST['fb_id'])
        except accounts_models.InviteRequest.DoesNotExist:
            return HttpResponseBadRequest('User has not submitted an invite request')

        inv_req.vanish()
        return HttpResponse('Invite request with FB ID %s has been deleted!' % request.POST['fb_id'])

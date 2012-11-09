from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import redirect
from django.conf import settings
import urllib
import cgi
import json

import base.api.base as base
import accounts.models as accounts_models
import accounts.forms as accounts_forms

class InviteCreateApi(base.RestView):

    model = accounts_models.InviteRequest
    form = accounts_forms.InviteCreateForm

    def POST(self, request, *args, **kwargs):
        if 'fb_id' not in request.POST or not request.POST['name']:
            return HttpResponseBadRequest('Please sign into Facebook and authorize the app to request an invite.')
        if 'name' not in request.POST or not request.POST['name']:
            return HttpResponseBadRequest('A name is required for requesting an invite.')
        if 'email' not in request.POST or not request.POST['email']:
            return HttpResponseBadRequest('An email is required for requesting an invite.')
        if 'description' not in request.POST or not request.POST['description']:
            return HttpResponseBadRequest('A source is required for requesting an invite.')
        form = accounts_forms.InviteCreateForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest('{%s}: {%s}' %
                (form.fields[form.errors.keys()[0]].label, form.errors.values()[0][0]))
        fields = form.cleaned_data

        try:
            invite_req = accounts_models.InviteRequest.objects.get(email=fields['email'])
            return HttpResponseBadRequest('You have already submitted an invite request.')
        except accounts_models.InviteRequest.DoesNotExist:
            new_req = accounts_models.InviteRequest(**fields)
            new_req.save()
            return HttpResponse('Request received!')

class InviteApi(base.RestView):

    model = accounts_models.InviteRequest

    def GET(self, request, *args, **kwargs):
        args = {
            client_id: settings.FACEBOOK_APP_ID,
            redirect_uri: settings.DOMAIN + 'api/accounts/request/invite/'
        }
        if 'code' not in request.GET or not request.GET['code']:
            args['scope'] = 'email,user_birthday,user_location,read_stream'
            return redirect('https://graph.facebook.com/oauth/authorize?' +
                urllib.urlencode(args))
        else:
            args['client_secret'] = settings.FACEBOOK_APP_SECRET
            args['code'] = request.GET.get('code')
            response = cgi.parse_qs(urllib.urlopen(
                'https://graph.facebook.com/oauth/access_token?' +
                urllib.urlencode(args)).read())
            access_token = response['access_token'][-1]
                if 'access_token' in response else None
            profile = json.load(urllib.urlopen('https://graph.facebook.com/me?' +
                urllib.urlencode(dict(access_token=access_token))))
            print profile
        return HttpResponse()


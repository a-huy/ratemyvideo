import datetime
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, \
    HttpResponseForbidden
from django.shortcuts import redirect

import base.api.base as base
import accounts.models as accounts_models
import accounts.forms as accounts_forms
import accounts.lib.invite as invite_lib
from base.contrib import whitelisted

class UserUpdateApi(base.RestView):

    model = accounts_models.User
    form = accounts_forms.UserUpdateForm

    def GET(self, request, fb_id, *args, **kwargs):

        try:
            user = accounts_models.User.objects.get(fb_id=fb_id)
        except accounts_models.User.DoesNotExist:
            return HttpResponseBadRequest('Invalid id')
        if not whitelisted(fb_id):
            return HttpResponseForbidden('User has not been authenticated')
        request.session['fb_id'] = fb_id
        return base.APIResponse(user.json_safe())

    def PUT(self, request, fb_id, *args, **kwargs):
        return HttpReponse()

    def DELETE(self, request, fb_id, *args, **kwargs):
        del request.session['fb_id']
        return HttpResponse()


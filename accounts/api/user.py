from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest

import base.api.base as base
import accounts.models as accounts_models
import accounts.forms as accounts_forms

class UserCreateApi(base.RestView):

    model = accounts_models.User
    form = accounts_forms.UserCreateForm

    def POST(self, request, *args, **kwargs):
        return HttpResponse()
        
class UserApi(base.RestView):

    model = accounts_models.User
    form = accounts_forms.UserUpdateForm

    def PUT(self, request, user_id, *args, **kwargs):
        return HttpReponse()
    
    def DELETE(self, request, user_id, *args, **kwargs):
        return HttpResponse()


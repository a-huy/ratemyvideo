from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest

import base.api.base as base
import accounts.models as accounts_models
import accounts.forms as accounts_forms

class UserCreateApi(base.RestView):

    model = accounts_models.User
    form = accounts_forms.UserCreateForm

    def POST(self, request, *args, **kwargs):
        if 'fb_id' not in request.POST or not request.POST['fb_id']:
            return HttpResponseBadRequest('A Facebook ID is required')
        if 'real_name' not in request.POST or not request.POST['real_name']:
            return HttpResponseBadRequest('User\'s real name is required')
        form = accounts_forms.UserCreateForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest('{%s}: {%s}' % 
                (form.fields[form.errors.keys()[0].label, 
                 form.errors.values()[0][0]))
        
        fields = form.cleaned_data
        
        try:
            account = accounts_models.User.get(fb_id=fields['fb_id'])
            # return video queue
            return HttpResponse() 
        except accounts_models.User.DoesNotExist:
            new_user = accounts_models.User(**fields)
            new_user.save()   
            
        # return video queue
        
class UserUpdateApi(base.RestView):

    model = accounts_models.User
    form = accounts_forms.UserUpdateForm

    def PUT(self, request, user_id, *args, **kwargs):
        return HttpReponse()
    
    def DELETE(self, request, user_id, *args, **kwargs):
        return HttpResponse()


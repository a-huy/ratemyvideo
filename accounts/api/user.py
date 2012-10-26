import datetime
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
        if 'location' not in request.POST or not request.POST['location']:
            return HttpResponseBadRequest('User\'s location is required')
        if 'birthday' not in request.POST or not request.POST['birthday']:
            return HttpResponseBadRequest('User\'s birthday is required')
        form = accounts_forms.UserCreateForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest('{%s}: {%s}' % 
                (form.fields[form.errors.keys()[0]].label, form.errors.values()[0][0]))
        fields = form.cleaned_data
        
        try:
            account = accounts_models.User.objects.get(fb_id=fields['fb_id'])
            request.session['fb_id'] = account.fb_id
            return base.APIResponse(account.to_json())
        except accounts_models.User.DoesNotExist:
            new_user = accounts_models.User(**fields)
            new_user.earned = 00.00
            new_user.rated = 0
            new_user.liked = 0
            new_user.commented = 0
            if request.POST['birthday'] == 'undefined':
                new_user.age = 0
            else:
                birthday = request.POST['birthday'].split('/')
                today = datetime.datetime.today()
                new_user.age = today.year - int(birthday[2])
                if (today.month, today.day) < (int(birthday[0]), int(birthday[1])):
                    new_user.age -= 1
            new_user.save()
            request.session['fb_id'] = new_user.fb_id
        return base.APIResponse(new_user.to_json())
        
class UserUpdateApi(base.RestView):

    model = accounts_models.User
    form = accounts_forms.UserUpdateForm

    def GET(self, request, fb_id, *args, **kwargs):
        
        try:
            user = accounts_models.User.objects.get(fb_id=fb_id)
        except accounts_models.User.DoesNotExist:
            return HttpResponseBadRequest('Invalid id')
        
        return base.APIResponse(user.to_json())
        
    def PUT(self, request, fb_id, *args, **kwargs):
        return HttpReponse()
    
    def DELETE(self, request, fb_id, *args, **kwargs):
        return HttpResponse()


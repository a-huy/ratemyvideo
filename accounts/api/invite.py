from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest

import base.api.base as base
import accounts.models as accounts_models
import accounts.forms as accounts_forms

class InviteCreateApi(base.RestView):

    model = accounts_models.InviteRequest
    form = accounts_forms.InviteCreateForm

    def POST(self, request, *args, **kwargs):
        if 'name' not in request.POST or not request.POST['name']:
            return HttpResponseBadRequest('A name is required for requesting an invite')
        if 'email' not in request.POST or not request.POST['email']:
            return HttpResponseBadRequest('An email is required for requesting an invite')
        if 'description' not in request.POST or not request.POST['description']:
            return HttpResponseBadRequest('A source is required for requesting an invite')
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


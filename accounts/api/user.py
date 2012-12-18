import datetime
from decimal import *
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, \
    HttpResponseForbidden
from django.shortcuts import redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.db.models import Max

import base.api.base as base
import accounts.models as accounts_models
import accounts.forms as accounts_forms
import accounts.lib.invite as invite_lib
import accounts.lib.user as user_lib
from base.contrib import whitelisted

class UserUpdateApi(base.RestView):

    model = accounts_models.User
    form = accounts_forms.UserUpdateForm

    def GET(self, request, fb_id, *args, **kwargs):

        try:
            user = accounts_models.User.objects.get(fb_id=fb_id)
        except accounts_models.User.DoesNotExist:
            return HttpResponseForbidden('User has not been authenticated')
        if not whitelisted(fb_id):
            return HttpResponseForbidden('User has not been authenticated')
        request.session['fb_id'] = fb_id
        po_dates = list(accounts_models.Payout.active.filter(user=user).values_list('created_date', flat=True).order_by('-created_date'))
        po_dates += [user.created_date]
        avg_po_time = user_lib.avg_payout_time(po_dates)
        tslp = user_lib.time_since_last_payout(po_dates)
        data = user.json_safe()
        data['avg_po_time'] = '%s|%s' % (avg_po_time.days, tslp.seconds / 3600) if avg_po_time else 'N/A'
        data['tslp'] = '%s|%s' % (tslp.days, tslp.seconds / 3600) if tslp else 'N/A'
        return base.APIResponse(data)

    def PUT(self, request, fb_id, *args, **kwargs):
        if not request.user.is_authenticated(): redirect('/rmvadmin/')
        try:
            user = accounts_models.User.objects.get(fb_id=fb_id)
        except accounts_models.User.DoesNotExist:
            return HttpResponseBadRequest('User with FB ID ' + fb_id + ' does not exist')
        if 'verified' in request.POST and request.POST['verified']:
            user.verified = True if request.POST['verified'] == 'true' else False
        if 'real_name' in request.POST and request.POST['real_name']:
            user.real_name = user_lib.capitalize_name(request.POST['real_name'])
        if 'balance' in request.POST and request.POST['balance']:
            try:
                if user.balance != Decimal(request.POST['balance']):
                    user.balance = Decimal(request.POST['balance'])
            except InvalidOperation:
                return HttpResponseBadRequest('The balance amount is not a valid number')
        if 'pp_email' in request.POST and request.POST['pp_email']:
            try:
                validate_email(request.POST['pp_email'])
                user.pp_email = request.POST['pp_email']
            except ValidationError:
                return HttpResponseBadRequest('The Paypal email you have submitted ' + \
                    'is not a valid email')
        user.save()
        return base.APIResponse({ })


    def DELETE(self, request, fb_id, *args, **kwargs):
        del request.session['fb_id']
        return HttpResponse()


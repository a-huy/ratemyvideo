import datetime
from decimal import *
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, \
    HttpResponseForbidden
from django.shortcuts import redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.utils.timezone import now
from django.db.models import Max

import base.api.base as base
import accounts.models as accounts_models
import accounts.forms as accounts_forms
import accounts.lib.invite as invite_lib
import accounts.lib.user as user_lib
import base.cache_keys as cache_keys
from base.contrib import whitelisted

class UserUpdateApi(base.RestView):

    model = accounts_models.User
    form = accounts_forms.UserUpdateForm

    def GET(self, request, fb_id, *args, **kwargs):
        try:
            user = accounts_models.User.objects.get(fb_id=fb_id)
        except accounts_models.User.DoesNotExist:
            return HttpResponseForbidden('User is not registered')
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
        session = request.session
        if not request.user.is_authenticated():
            if 'fb_id' not in session or session['fb_id'] == -1 or session['fb_id'] != fb_id:
                return HttpResponseForbidden()
        try:
            if request.user.is_authenticated(): user = accounts_models.User.objects.get(fb_id=fb_id)
            else: user = accounts_models.User.objects.get(fb_id=session['fb_id'])
        except accounts_models.User.DoesNotExist:
            return HttpResponseBadRequest('The user you are looking for does not exist!')
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
        if 'email' in request.POST:
            try:
                validate_email(request.POST['email'])
                user.email = request.POST['email']
            except ValidationError:
                return HttpResponseBadRequest('The email you have submitted is not a valid address.')
        if 'pp_email' in request.POST:
            try:
                validate_email(request.POST['pp_email'])
                user.pp_email = request.POST['pp_email']
            except ValidationError:
                return HttpResponseBadRequest('The Paypal email you have submitted ' + \
                    'is not a valid email address.')
        user.save()
        cache.delete(cache_keys.PAGECACHE % ('rmvadmin:edit:user:%s' % user.fb_id))
        return base.APIResponse({ })

    def DELETE(self, request, fb_id, *args, **kwargs):
        del request.session['fb_id']
        return HttpResponse()


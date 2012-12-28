from decimal import *
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import redirect

import base.api.base as base

import accounts.models as accounts_models

class PayoutCreateApi(base.RestView):

    model = accounts_models.Payout

    def POST(self, request, *args, **kwargs):
        if not request.user.is_authenticated(): return redirect('/rmvadmin/')
        if 'amount' not in request.POST or not request.POST['amount']:
            return HttpResponseBadRequest('An amount must be specified')
        if 'fb_id' not in request.POST or not request.POST['fb_id']:
            return HttpResponseBadRequest('A user must be specified')
        try:
            user = accounts_models.User.active.get(fb_id=request.POST['fb_id'])
            amount = Decimal(request.POST['amount'])
        except accounts_models.User.DoesNotExist:
            return HttpResponseBadRequest('A user with the specified FB ID does not exist')
        except InvalidOperation:
            return HttpResponseBadRequest('A decimal number could not be extracted ' +
                'from the submitted amount')

        if user.balance < amount:
            return HttpResponseBadRequest('Submitted amount is larger than %s\'s balance' % user.real_name)
        user.balance = round(user.balance - amount, 2)
        if not user.verified: user.verified = True
        user.save()

        args = {
            'user': user,
            'amount': amount
        }
        payout = accounts_models.Payout(**args)
        payout.save()

        return HttpResponse('Payout has been successfully submitted!')

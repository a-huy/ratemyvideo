from django.conf import settings
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404, \
    HttpResponse
from django.template import RequestContext

import urllib
import accounts.lib.invite as invite_lib
from base.contrib import whitelisted

def login_page(request):
    context_vars = { 'status':'out' }
    context_vars['json_vars'] = {
        'APP_ID': settings.FACEBOOK_APP_ID,
        'DOMAIN': settings.DOMAIN,
        'SCOPE': settings.FACEBOOK_SCOPE,
        'CHANNEL': settings.DOMAIN + 'login/channel/'
    }
    if 'error_reason' in request.GET and request.GET['error_reason'] == 'user_denied':
        context_vars['status'] = 'user_denied'
        return render_to_response('login_page.html', context_vars,
            context_instance=RequestContext(request))
    if 'code' not in request.GET or not request.GET['code']:
        return render_to_response('login_page.html', context_vars,
            context_instance=RequestContext(request))
    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': settings.DOMAIN + 'login/',
        'code': request.GET.get('code')
    }
    user = invite_lib.get_user_data(args, request)
    if not whitelisted(user['fb_id']): return redirect('invite_required')
    request.session['fb_id'] = user['fb_id']
    context_vars['status'] = 'in'
    context_vars['name'] = user['real_name']
    return render_to_response('login_page.html', context_vars,
        context_instance=RequestContext(request))

def channel(request):
    return render(request, 'channel.html', { })

def invite_required(request):
    context_vars = { 'home_url': settings.DOMAIN }
    return render_to_response('invite_required.html', context_vars,
        context_instance=RequestContext(request))


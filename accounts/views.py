from django.conf import settings
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404, \
    HttpResponse
from django.template import RequestContext

import urllib
import accounts.lib.invite as invite_lib

def login_page(request):
    context_vars = { 'status':'out' }
    if 'code' not in request.GET or not request.GET['code']:
        return render_to_response('login_page.html', context_vars,
            context_instance=RequestContext(request))
    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': settings.DOMAIN + 'login/',
        'code': request.GET.get('code')
    }
    user = invite_lib.get_user_data(args)
    request.session['fb_id'] = user['fb_id']
    context_vars['status'] = 'in'
    context_vars['name'] = user['real_name']
    return render_to_response('login_page.html', context_vars,
        context_instance=RequestContext(request))

def channel(request):
    return render(request, 'channel.html', { })


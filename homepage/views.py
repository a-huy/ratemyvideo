from django.conf import settings
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404, \
    HttpResponse
from django.template import RequestContext

def homepage(request):
    context_vars = {
        'json_vars': {
            'APP_ID': settings.FACEBOOK_APP_ID,
            'RED_URL': settings.DOMAIN + 'api/accounts/request/invite/',
            'SCOPE': settings.FACEBOOK_SCOPE
        }
    }
    return render_to_response('homepage.html', context_vars,
        context_instance=RequestContext(request))


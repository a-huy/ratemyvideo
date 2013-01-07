from django.conf import settings
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404, \
    HttpResponse
from django.template import RequestContext
from base.decorators import pagecache

@pagecache('homepage')
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

@pagecache('privacy-policy')
def privacy_policy(request):
    context_vars = {
    }
    return render_to_response('privacy_policy.html', context_vars,
        context_instance=RequestContext(request))

@pagecache('terms-of-service')
def terms_of_service(request):
    context_vars = {
    }
    return render_to_response('terms_of_service.html', context_vars,
        context_instance=RequestContext(request))
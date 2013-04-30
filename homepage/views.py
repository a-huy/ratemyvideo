from django.conf import settings
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404, \
    HttpResponse
from django.template import RequestContext
from django.core.mail import send_mail, BadHeaderError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from base.decorators import pagecache

# @pagecache('homepage')
def homepage(request):
    context_vars = {
        'json_vars': {
            'APP_ID': settings.FACEBOOK_APP_ID,
            'RED_URL': settings.DOMAIN + 'api/accounts/request/invite/',
            'SCOPE': settings.FACEBOOK_SCOPE
        }
    }
    return render_to_response('landing_page.html', context_vars,
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

@pagecache('faq')
def faq(request):
    context_vars = { }
    return render_to_response('faq.html', context_vars,
        context_instance=RequestContext(request))

@pagecache('about')
def about(request):
    context_vars = { }
    return render_to_response('about.html', context_vars,
        context_instance=RequestContext(request))

def signup(request):
    context_vars = {
        'json_vars': {
            'APP_ID': settings.FACEBOOK_APP_ID,
            'RED_URL': settings.DOMAIN + 'api/accounts/request/invite/',
            'SCOPE': settings.FACEBOOK_SCOPE
        }
    }
    return render_to_response('signup.html', context_vars,
        context_instance=RequestContext(request))

def comment(request):
    if 'name' not in request.POST:
        return HttpResponseBadRequest('Please include your name.')
    if 'email' not in request.POST:
        return HttpResponseBadRequest('Please submit an email.')
    if 'comment' not in request.POST:
        return HttpResponseBadRequest('Please submit a comment.')
    try:
        validate_email(request.POST['email'])
        send_mail('Comment from %s' % request.POST['name'], request.POST['comment'],
            request.POST['email'], ['support@ratemyvideo.co'])
    except BadHeaderError:
        return HttpResponseServerError('Sorry, something went wrong. Please try again later.')
    except ValidationError:
        return HttpResponseBadRequest('Please submit a valid email.')
    return HttpResponse()
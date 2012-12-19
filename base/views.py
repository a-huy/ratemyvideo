from django.conf import settings
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404, \
    HttpResponse
from django.template import RequestContext

def download_extension(request):
    return redirect('/content/assets/static/files/ratemyvideo.crx')

# Custom HttpResponse Page
def message_response(request, code, msg):
    context_vars = { 'message': msg }
    response = render_to_response('message.html', context_vars,
        context_instance=RequestContext(request))
    response.status_code = code
    return response

def custom_500(request):
    response = render_to_response('500.html', { },
        context_instance=RequestContext(request))
    response.status_code = 500
    return response
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404, \
    HttpResponse
from django.template import RequestContext

def homepage(request):
    return render_to_response('homepage.html', { }, 
        context_instance=RequestContext(request))


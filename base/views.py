from django.conf import settings
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404, \
    HttpResponse
from django.template import RequestContext

def download_extension(request):
    return redirect('/content/assets/static/files/ratemyvideo.crx')


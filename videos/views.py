from django.conf import settings
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.template import RequestContext

def video_page(request, video_id):
    template_vars = {
        'video_id': video_id
    }
    return render(request, 'video_page.html', template_vars)
    


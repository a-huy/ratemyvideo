from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest

import base.api.base as base

class SessionApi(base.RestView):

    def GET(self, request, *args, **kwargs):
        
        if 'fb_id' not in request.session:
            data = { 'fb_id': '-1' }
        else: data = { 'fb_id': request.session['fb_id'] }
        
        return base.APIResponse(data)

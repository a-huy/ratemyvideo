from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest

import base.api.base as base

class SessionApi(base.RestView):

    def GET(self, request, *args, **kwargs):
        
        if not request.session['fb_id']:
            return HttpResponseBadRequest('User not signed in');
        data = {
            'fb_id': request.session['fb_id']
        }
        
        return base.APIResponse(data)

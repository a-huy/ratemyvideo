from django.http import Http404, HttpRequest, HttpResponse, HttpResponseNotAllowed, \
    HttpResponseBadRequest, HttpResponseForbidden
from django.core.serializers.json import DjangoJSONEncoder
    
class RestView(object):
    
    def __new__(cls, request, *args, **kwargs):
        view = cls.new(request, *args, **kwargs)
        return view.dispatch(request, *args, **kwargs)
        
    def dispatch(self, request, *args, **kwargs):
        method = request.META.get('HTTP_X_HTTP_METHOD_OVERRIDE', request.method)
        
        _METHODS = ('GET', 'PUT', 'DELETE', 'UNDELETE')
        if not method in _METHODS:
            return HttpResponseBadRequest()
        try:
            return getattr(self, method)(request, *args, **kwargs)
        except NotImplementedError:
            methods = [getattr(self, m) for m in _METHODS if hasattr(self, m)]
            methods = [m.__name__ for m in methods if getattr(m, '_impl', True)]
            return HttpResponseNotAllowed(methods)

    @classmethod
    def new(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj.__init__(*args, **kwargs)
        return obj
        
    def __init__(self, *args, **kwargs):
        super(RestView, self).__init__()
        
    def GET(self, request, *args, **kwargs):
        raise NotImplementedError
   
    def PUT(self, request, *args, **kwargs):
        raise NotImplementedError
        
    def POST(self, request, *args, **kwargs):
        raise NotImplementedError
        
    def DELETE(self, request, *args, **kwargs):
        raise NotImplementedError
        
    def UNDELETE(self, request, *args, **kwargs):
        raise NotImplementedError
        
    GET._impl = False
    PUT._impl = False
    POST._impl = False
    DELETE._impl = False
    UNDELETE._impl = False
    
def APIResponse(data, status_code=200, response_type='json', cookie=None):
    mimetypes = \
    {
        'json': 'application/json'
    }
    content = json.dumps(data, cls=DjangoJSONEncoder)
    response = HttpResponse(content, mimetype=mimetypes[response_type])
    if cookie:
        response.set_cookie(cookie['key'], value=cookie['value'])
        
    return response


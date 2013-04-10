from django.http import HttpRequest, HttpResponseBadRequest
import base.api.base as base
import accounts.models as accounts_models
import hashlib

class BanApi(base.RestView):

    def POST(self, request, fb_id, *args, **kwargs):
        if not request.user.is_authenticated(): return
        try:
            user = accounts_models.User.active.get(fb_id=fb_id)
        except accounts_models.User.DoesNotExist:
            return HttpResponseBadRequest('User could not be found.')

        hash_key = hashlib.sha512('rmv:whitelist:%s' % fb_id).hexdigest()
        try:
            entry = accounts_models.UserWhiteList.active.get(key=hash_key)
        except accounts_models.UserWhitelist.DoesNotExist:
            return HttpResponseBadRequest('User is not whitelisted.')

        user.vanish()
        entry.vanish()

        return HttpResponse()

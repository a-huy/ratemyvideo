import hashlib
import copy

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.conf import settings

import base.api.base as base
import accounts.models as accounts_models
import accounts.forms as accounts_forms
import accounts.lib.whitelist as whitelist_lib
from base.tasks import send_email


class WhiteListCreateApi(base.RestView):

    model = accounts_models.UserWhitelist

    def POST(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden('User is not logged in')
        if 'fb_id' not in request.POST or not request.POST['fb_id']:
            return HttpResponseBadRequest('A whitelist seed is required')
        try:
            inv_req = accounts_models.InviteRequest.active.get(fb_id=request.POST['fb_id'])
            curr_user = accounts_models.User.active.get(fb_id=request.POST['fb_id'])
            return HttpResponseBadRequest('User is already registered with the service')
        except accounts_models.InviteRequest.DoesNotExist:
            return HttpResponseBadRequest('Invite request could not be found')
        except accounts_models.User.DoesNotExist:
            pass

        # Create a new User out of the request
        inv_req_dict = copy.deepcopy(inv_req.__dict__)
        del inv_req_dict['reason']
        del inv_req_dict['_state']
        new_user = accounts_models.User(**inv_req_dict)
        # Save the User, remove the request
        new_user.save()
        inv_req.vanish()
        # Create a video queue for the new user
        whitelist_lib.create_queue(new_user)

        # Update the whitelist
        hash_key = hashlib.sha512('rmv:whitelist:' + new_user.fb_id).hexdigest()
        fields = {
            'key': hash_key
        }
        new_entry = accounts_models.UserWhitelist(**fields)
        new_entry.save()

        send_email.delay('welcome_user', new_user.email, [new_user.real_name, settings.DOMAIN, new_user.email])

        return HttpResponse('The whitelist has been updated!')

import hashlib

import accounts.models as accounts_models

# Determines if a particular Facebook ID is whitelisted
def whitelisted(fb_id):
    hash_key = hashlib.sha512('rmv:whitelist:%s' % fb_id).hexdigest()
    try:
        entry = accounts_models.UserWhitelist.active.get(key=hash_key)
        return True
    except accounts_models.UserWhitelist.DoesNotExist:
        return False

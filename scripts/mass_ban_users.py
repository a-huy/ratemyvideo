#!/usr/bin/env/python

import utils.djangoenv
import accounts.models as am
import hashlib
import sys
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def ban_users(infile):
    with open(infile) as banlist:
        for email in banlist:
            try:
                email = email.strip()
                validate_email(email)
                user = am.User.active.get(email=email)
                hk = hashlib.sha512('rmv:whitelist:%s' % user.fb_id).hexdigest()
                wl = am.UserWhitelist.active.get(key=hk)
                user.vanish()
                wl.vanish()
            except am.User.DoesNotExist:
                print 'User object with email %s could not be found' % email
            except am.UserWhitelist.DoesNotExist:
                print 'Whitelist object with email %s could not be found' % email
            except ValidationError:
                print '%s is not a valid email' % email

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: python mass_ban_users.py [email list file]'
        exit()
    ban_users(sys.argv[1])

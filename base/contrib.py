import hashlib
import re

from django.core.mail import send_mail, mail_admins, BadHeaderError

import base.email_templates as emails
import accounts.models as accounts_models

# Determines if a particular Facebook ID is whitelisted
def whitelisted(fb_id):
    hash_key = hashlib.sha512('rmv:whitelist:%s' % fb_id).hexdigest()
    try:
        entry = accounts_models.UserWhitelist.active.get(key=hash_key)
        return True
    except accounts_models.UserWhitelist.DoesNotExist:
        return False

# Send an email with a specified template
def send_email(template_name, recipient, email_args):
    if template_name not in emails.email_types:
        raise LookupError('Email template type not supported')
    template = emails.email_types[template_name]['template']
    try:
        send_mail(emails.email_types[template_name]['subject'],
            template % tuple(email_args), 'ratemyvideos@gmail.com', [recipient])
    except TypeError:
        raise TypeError('One or more email arguments are invalid')
    except BadHeaderError:
       raise BadHeaderError('Invalid header found.')

# Send an email to the admins, managers, or both
def backend_email(template_name, group_type, email_args):
    if template_name not in emails.email_types:
        raise LookupError('Email template type not supported')
    template = emails.email_types[template_name]['template']
    subject = emails.email_types[template_name]['subject']
    try:
        message = template % tuple(email_args)
        if 'admins' in group_type: mail_admins(subject, message)
        if 'managers' in group_type: mail_managers(subject, message)
    except TypeError:
        raise TypeError('One or more email arguments are invalid')
    except BadHeaderError:
       raise BadHeaderError('Invalid header found.')

# Check if a YouTube ID is in the correct format
def valid_yt_id(yt_id):
    return re.match(r'[a-zA-Z0-9\-\_]', yt_id)

# Converts a timedelta object into an integer representing the number of seconds
def timedelta_to_seconds(delta):
    return delta.days * 86400 + delta.seconds + (1 if delta.microseconds > 500000 else 0)


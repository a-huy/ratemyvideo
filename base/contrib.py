import hashlib
import smtplib
from email.mime.text import MIMEText

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
def send_email(template_name, recipient, *args):
    if template_name not in emails.email_types:
        raise LookupError('Email template type not supported')
    template = emails.email_types[template_name]['template']
    try:
        msg = MIMEText(template % tuple(args))
    except TypeError:
        raise TypeError('One or more string arguments are invalid')
    msg['Subject'] = emails.email_types[template_name]['subject']
    msg['From'] = 'ratemyvideos@gmail.com'
    msg['To'] = recipient

    letter = smtplib.SMTP('localhost')
    letter.sendmail('ratemyvideos@gmail.com', [recipient], msg.as_string())
    letter.quit()

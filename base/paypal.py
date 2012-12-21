# Utility class adapted from http://djangosnippets.org/snippets/1181/
# Used to automate user payouts

import urllib, hashlib
from django.utils.timezone import now
from django.conf import settings

class PayPal:
    credentials = {}
    API_ENDPOINT = ''
    API_URL = ''

    def __init__(self):
        self.credentials = {
            'USER': settings.TEST_PAYPAL_USER,
            'PWD': settings.TEST_PAYPAL_PASS,
            'SIGNATURE': settings.TEST_PAYPAL_SIGNATURE,
            'VERSION': settings.PAYPAL_API_VERSION
        }
        self.API_ENDPOINT = 'https://api-3t.sandbox.paypal.com/nvp' # Sandbox URL; TODO: CHANGE TO LIVE SITE
        # self.API_ENDPOINT = 'https://api-3t.paypal.com/nvp' # Live site URL
        self.PAYPAL_URL = 'https://www.sandbox.paypal.com/cgi-bin/webscr' # Sandbox URL; TODO: CHANGE TO LIVE SITE
        # self.PAYPAL_url = 'https://www.paypal.com/cgi-bin/webscr' # Live site URL
        self.signature = urllib.urlencode(self.credentials) + '&'

    def mass_pay(self, email, amt, note=None, email_subject=None):
        unique_id = str(hashlib.md5(str(now())).hexdigest())
        fields = {
            'METHOD': 'MassPay',
            'RECEIVERTYPE': 'EmailAddress',
            'CURRENCYCODE': 'USD',
            'L_EMAIL0': email,
            'L_AMT0': amt,
            'L_UNIQUE0': unique_id
        }
        if note: fields['L_NOTE0'] = note
        if email_subject: fields['EMAILSUBJECT'] = email_subject
        fields_str = self.signature + urllib.urlencode(fields)
        response = urllib.urlopen(self.API_ENDPOINT, fields_str).read()
        response_tokens = {}
        for token in response.split('&'):
            parts = token.split('=')
            response_tokens[parts[0]] = urllib.unquote(parts[1])
        response_tokens['unique_id'] = unique_id
        return response_tokens
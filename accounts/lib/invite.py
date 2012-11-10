import urllib
import json
import time
import cgi
from django.conf import settings

import accounts.models as accounts_models

# All the US states sans California and New York
states_whitelist = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "Colorado", "Connecticut",
    "Deleware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana",
    "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
    "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
    "Nevada", "New Hampshire", "New Jersey", "New Mexico", "North Carolina",
    "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island",
    "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

states_whitelist += ["California"] # For dev testing purposes, since we are... located in CA

def get_user_data(args):
    args['client_secret'] = settings.FACEBOOK_APP_SECRET
    response = cgi.parse_qs(urllib.urlopen(
        'https://graph.facebook.com/oauth/access_token?' +
        urllib.urlencode(args)).read())
    token_dict = {'access_token':response['access_token'][-1] \
        if 'access_token' in response else None }
    profile = json.load(urllib.urlopen('https://graph.facebook.com/me?' +
        urllib.urlencode(token_dict)))
    data = {
        'fb_id': profile['id'],
        'real_name': profile['name'],
        'location': profile['location']['name'],
        'birthday': profile['birthday'],
        'email': profile['email'],
        'gender': profile['gender'],
        'access_token': token_dict
    }
    return data

def account_is_eligible(user):
    """
        Returns a 2-type (is_eligible, reason), where:
            is_eligible : account is eligibile to use the extension
            reason : if is_eligibile is false, this is the error message
    """
    access_token = user['access_token']
    perms = json.load(urllib.urlopen(
        'https://graph.facebook.com/' + user['fb_id'] + '/permissions?' +
        urllib.urlencode(access_token)))
    if 'data' not in perms: return HttpResponseBadRequest('Bad Facebook ID or access token')
    if 'user_location' not in perms['data'][0]:
        return (False, 'Location permission not granted')
    if 'read_stream' not in perms['data'][0]:
        return (False, 'Reading user stream permission not granted')
    state = user['location'].split(',')[-1].strip()
    if state not in states_whitelist: return (False, 'User location "%s" not in authorized area' % user['location'])
    seconds_in_year = 60 * 60 * 24 * 365
    limit = int(round(time.time() - seconds_in_year))
    access_token['until'] = limit
    posts = json.load(urllib.urlopen(
        'https://graph.facebook.com/me/feed?' + urllib.urlencode(access_token)))
    if len(posts['data']) == 0: return (False, 'Account is less than a year old')
    return (True, '')


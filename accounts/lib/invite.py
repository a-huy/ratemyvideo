import urllib
import json
import time
import cgi
import datetime
import pygeoip
import os
from django.conf import settings

import accounts.models as accounts_models

# All the US states sans California
states_whitelist = {
    "Alabama":"AL", "Alaska":"AK", "Arizona":"AZ", "Arkansas":"AR", "Colorado":"CO",
    "Connecticut":"CT", "Deleware":"DE", "Florida":"FL", "Georgia":"GA", "Hawaii":"HI",
    "Idaho":"ID", "Illinois":"IL", "Indiana":"IN", "Iowa":"IA", "Kansas":"KS",
    "Kentucky":"KY", "Louisiana":"LA", "Maine":"ME", "Maryland":"MD", "Massachusetts":"MA",
    "Michigan":"MI", "Minnesota":"MN", "Mississippi":"MS", "Missouri":"MO",
    "Montana":"MT", "Nebraska":"NE", "Nevada":"NV", "New Hampshire":"NH", "New Jersey":"NJ",
    "New Mexico":"NM", "North Carolina":"NC", "North Dakota":"ND", "New York":"NY", "Ohio":"OH",
    "Oklahoma":"OK", "Oregon":"OR", "Pennsylvania":"PA", "Rhode Island":"RI",
    "South Carolina":"SC", "South Dakota":"SD", "Tennessee":"TN", "Texas":"TX",
    "Utah":"UT", "Vermont":"VT", "Virginia":"VA", "Washington":"WA", "West Virginia":"WV",
    "Wisconsin":"WI", "Wyoming":"WY"
}

#states_whitelist["California"] = "CA" # For dev testing purposes, since we are... located in CA

def is_inside_us(loc):
    return loc.split(', ')[-1] in (states_whitelist.keys() + ['California'])

def get_user_data(args, request):
    args['client_secret'] = settings.FACEBOOK_APP_SECRET
    response = cgi.parse_qs(urllib.urlopen(
        'https://graph.facebook.com/oauth/access_token?' +
        urllib.urlencode(args)).read())
    token_dict = {'access_token':response['access_token'][-1] \
        if 'access_token' in response else None }
    profile = json.load(urllib.urlopen('https://graph.facebook.com/me?' +
        urllib.urlencode(token_dict)))
    if 'location' in profile and profile['location']['name']:
        location = profile['location']['name']
    else: location = addr_to_loc(request)
    data = {
        'fb_id': profile['id'] if 'id' in profile else None,
        'real_name': profile['name'] if 'name' in profile else None,
        'location': location,
        'birthday': profile['birthday'] if 'birthday' in profile else 'undefined',
        'email': profile['email'] if 'email' in profile else None,
        'gender': profile['gender'] if 'gender' in profile else 'Unknown',
        'access_token': token_dict
    }
    return data

def account_is_eligible(user):
    """
        Returns a 2-tuple (is_eligible, reason), where:
            is_eligible : account is eligibile to use the extension
            reason : if is_eligibile is false, this is the error message
    """
    access_token = user['access_token']
    if not user['fb_id'] or not user['email'] or not user['real_name']:
        return (False, 'Please approve the requested permissions to use the service.')
    perms = json.load(urllib.urlopen(
        'https://graph.facebook.com/' + user['fb_id'] + '/permissions?' +
        urllib.urlencode(access_token)))
    if 'data' not in perms: return HttpResponseBadRequest('Bad Facebook ID or access token')
    if 'user_location' not in perms['data'][0]:
        return (False, 'Location permission not granted')
    if 'read_stream' not in perms['data'][0]:
        return (False, 'Reading user stream permission not granted')
    # Comment to allow int'l requests
#    state = user['location'].split(',')[-1].strip()
#    if state not in states_whitelist:
#        return (False, 'User location not in authorized area')
    if user['location'] == 'Unknown': return (False, 'User location not in authorized area')
    seconds_in_age_limit = 60 * 60 * 24 * 180 # It's actually about 6 months
    limit = int(round(time.time() - seconds_in_age_limit))
    access_token['until'] = limit
    posts = json.load(urllib.urlopen(
        'https://graph.facebook.com/me/feed?' + urllib.urlencode(access_token)))
    if 'data' not in posts or len(posts['data']) == 0:
        return (False, 'Account is less than 6 months old')
    return (True, '')

def create_request(user):
    del user['access_token']
    user['age'] = calc_age(user['birthday'])
    del user['birthday']
    new_req = accounts_models.InviteRequest(**user)
    new_req.save()

def calc_age(birthday):
    if birthday == 'undefined': return 0
    birthday = birthday.split('/')
    today = datetime.datetime.today()
    age = today.year - int(birthday[2])
    if (today.month, today.day) < (int(birthday[0]), int(birthday[1])): age -= 1
    return age

def addr_to_loc(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        addr = request.META.get('HTTP_X_FORWARDED_FOR').split(',')[-1].strip()
    else: addr = request.META.get('REMOTE_ADDR', '127.0.0.1')
    geoip = pygeoip.GeoIP(os.path.join(settings.GEOIP_PATH, 'GeoLiteCity.dat'))
    result = geoip.record_by_addr(addr)
    if not result: return 'Unknown'
    if result['country_code'] != 'US':
        loc_str = result['country_name']
        if result['region_name']: loc_str = result['region_name'] + ', ' + loc_str
        if result['city']: loc_str = result['city'] + ', ' + loc_str
        return loc_str
    state = filter(lambda x: states_whitelist[x] == result['region_name'], states_whitelist.keys())
    if not result['region_name'] or not state: return 'Unknown'
    return result['city'] + ', ' + state[0]


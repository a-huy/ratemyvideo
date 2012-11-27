import urllib
import json
import time
import cgi
import datetime
import pygeoip
import os
from django.conf import settings

import accounts.models as accounts_models

# All the US states sans California and New York
states_whitelist = {
    "Alabama":"AL", "Alaska":"AK", "Arizona":"AZ", "Arkansas":"AR", "Colorado":"CO",
    "Connecticut":"CT", "Deleware":"DE", "Florida":"FL", "Georgia":"GA", "Hawaii":"HI",
    "Idaho":"ID", "Illinois":"IL", "Indiana":"IN", "Iowa":"IA", "Kansas":"KS",
    "Kentucky":"KY", "Louisiana":"LA", "Maine":"ME", "Maryland":"MD", "Massachusetts":"MA",
    "Michigan":"MI", "Minnesota":"MN", "Mississippi":"MS", "Missouri":"MO",
    "Montana":"MT", "Nebraska":"NE", "Nevada":"NV", "New Hampshire":"NH", "New Jersey":"NJ",
    "New Mexico":"NM", "North Carolina":"NC", "North Dakota":"ND", "Ohio":"OH",
    "Oklahoma":"OK", "Oregon":"OR", "Pennsylvania":"PA", "Rhode Island":"RI",
    "South Carolina":"SC", "South Dakota":"SD", "Tennessee":"TN", "Texas":"TX",
    "Utah":"UT", "Vermont":"VT", "Virginia":"VA", "Washington":"WA", "West Virginia":"WV",
    "Wisconsin":"WI", "Wyoming":"WY"
}

states_whitelist["California"] = "CA" # For dev testing purposes, since we are... located in CA

def get_user_data(args, request):
    args['client_secret'] = settings.FACEBOOK_APP_SECRET
    response = cgi.parse_qs(urllib.urlopen(
        'https://graph.facebook.com/oauth/access_token?' +
        urllib.urlencode(args)).read())
    token_dict = {'access_token':response['access_token'][-1] \
        if 'access_token' in response else None }
    profile = json.load(urllib.urlopen('https://graph.facebook.com/me?' +
        urllib.urlencode(token_dict)))
    location = profile['location']['name'] if 'location' in profile else addr_to_us_loc(request.META['REMOTE_ADDR'])
    data = {
        'fb_id': profile['id'],
        'real_name': profile['name'],
        'location': location,
        'birthday': profile['birthday'] if 'birthday' in profile else 'undefined',
        'email': profile['email'],
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
    perms = json.load(urllib.urlopen(
        'https://graph.facebook.com/' + user['fb_id'] + '/permissions?' +
        urllib.urlencode(access_token)))
    if 'data' not in perms: return HttpResponseBadRequest('Bad Facebook ID or access token')
    if 'user_location' not in perms['data'][0]:
        return (False, 'Location permission not granted')
    if 'read_stream' not in perms['data'][0]:
        return (False, 'Reading user stream permission not granted')
    state = user['location'].split(',')[-1].strip()
    if state not in states_whitelist:
        return (False, 'User location not in authorized area')
    seconds_in_year = 60 * 60 * 24 * 90
    limit = int(round(time.time() - seconds_in_year))
    access_token['until'] = limit
    posts = json.load(urllib.urlopen(
        'https://graph.facebook.com/me/feed?' + urllib.urlencode(access_token)))
    if len(posts['data']) == 0: return (False, 'Account is less than a year old')
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

def addr_to_us_loc(addr):
    geoip = pygeoip.GeoIP(os.path.join(settings.GEOIP_PATH, 'GeoLiteCity.dat'))
    result = geoip.record_by_addr(addr)
    if not result or result['country_code'] != 'US': return 'Unknown'
    return result['city'] + ', ' + \
        filter(lambda x: states_whitelist[x] == result['region_name'], states_whitelist.keys())[0]


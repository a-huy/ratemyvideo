import hashlib
import re
import datetime

from django.utils.timezone import now

import accounts.models as accounts_models
import videos.models as videos_models

# Determines if a particular Facebook ID is whitelisted
def whitelisted(fb_id):
    hash_key = hashlib.sha512('rmv:whitelist:%s' % fb_id).hexdigest()
    try:
        entry = accounts_models.UserWhitelist.active.get(key=hash_key)
        return True
    except accounts_models.UserWhitelist.DoesNotExist:
        return False

# Check if a YouTube ID is in the correct format
def valid_yt_id(yt_id):
    return re.match(r'[a-zA-Z0-9\-\_]', yt_id)

# Converts a timedelta object into an integer representing the number of seconds
def timedelta_to_seconds(delta):
    return delta.days * 86400 + delta.seconds + (1 if delta.microseconds > 500000 else 0)

# Extracts an IP Address from a request object. Returns None if it could not
def extract_addr(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META.get('HTTP_X_FORWARDED_FOR').split(',')[-1].strip()
    return request.META.get('REMOTE_ADDR', None)

# Calculates the amount of time that has elapsed since a user's last video rating
def time_since_last_rating(pk):
    tslr = datetime.timedelta(999999999)
    user_ratings = videos_models.Rating.active.filter(user_id=pk).order_by('-created_date')
    if len(user_ratings) != 0: tslr = now() - user_ratings[0].created_date
    return tslr

# Calculates the Damerau-Levenshtein Distance (allows for transpositions)
# I didn't want to download an entire module just for a single function
def calc_dld(source, target):

    # I didn't want to import a module for this
    def matrix(rows, cols, default=0):
        mat = []
        for argi in xrange(rows):
            row = []
            for argt in xrange(cols): row.append(default)
            mat.append(row)
        return mat

    # Handle the trivial cases
    if not source:
        if not target: return 0
        else: return len(target)
    elif not target: return len(source)

    # Create and setup the score matrix
    score = matrix(len(source) + 2, len(target) + 2)
    INF = len(source) + len(target)
    score[0][0] = INF
    for argi in xrange(len(source) + 1):
        score[argi + 1][1] = argi
        score[argi + 1][0] = INF
    for argt in xrange(len(target) + 1):
        score[1][argt + 1] = argt
        score[0][argt + 1] = INF

    # Setup alphabet dict
    alpha = { }
    for char in source + target:
        if char not in alpha: alpha[char] = 0

    for argi in xrange(1, len(source) + 1):
        DB = 0
        for argt in xrange(1, len(target) + 1):
            argi1 = alpha[target[argt - 1]]
            argt1 = DB

            if source[argi - 1] == target[argt - 1]:
                score[argi + 1][argt + 1] = score[argi][argt]
                DB = argt
            else:
                score[argi + 1][argt + 1] = \
                    min(score[argi][argt], min(score[argi + 1][argt], score[argi][argt + 1])) + 1
            score[argi + 1][argt + 1] = \
                min(score[argi + 1][argt + 1],
                    score[argi1][argt1] + (argi - argi1 - 1) + 1 + (argt - argt1 - 1))
        alpha[source[argi - 1]] = argi

    print_matrix(score)
    return score[len(source) + 1][len(target) + 1]


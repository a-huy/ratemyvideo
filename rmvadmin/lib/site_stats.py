from django.core.cache import cache
from django.utils.timezone import now
from django.conf import settings
import pytz
import datetime
import collections
import accounts.models as accounts_models
import videos.models as videos_models
import base.cache_keys as keys

# grabs a graph's data from cache
def get_graph_data(key):
    date_today = now().strftime('%m-%d-%Y')
    graph_key = key % date_today
    return cache.get(key)

# puts a graph's data in cache
def set_graph_data(key, data, exp_time):
    date_today = now().strftime('%m-%d-%Y')
    graph_key = key % date_today
    cache.set(key, data, exp_time)

# takes a list of datetime objects and returns a list of [date, count]
def count_by_date(items):
    adj_dates = []
    for date in items: adj_dates.append(date - datetime.timedelta(hours=8)) # UTC to PST
    dates_list = []
    counts = collections.Counter([datetime.datetime(month=x.month, \
        day=x.day, year=x.year) for x in adj_dates])
    map(lambda x: dates_list.append(['%s-%s-%s' % (x.month, x.day, x.year),
        counts[x]]), sorted(list(counts)))
    return dates_list

# gets the number of ratings per day as a list
def ratings_day_count(invalidate=False):
    if not invalidate:
        graph_data = get_graph_data(keys.RMV_RATING_DATES)
        if graph_data: return graph_data
    
    values = videos_models.Rating.active.values_list('created_date', flat=True)
    dates_list = count_by_date(values)
    set_graph_data(keys.RMV_RATING_DATES, dates_list, 3600 * 3)
    return dates_list

# gets the number of new users per day as a list
def new_users_day_count(invalidate=False):
    if not invalidate:
        graph_data = get_graph_data(keys.RMV_USER_DATES)
        if graph_data: return graph_data

    values = accounts_models.User.active.values_list('created_date', flat=True)
    dates_list = count_by_date(values)
    set_graph_data(keys.RMV_USER_DATES, dates_list, 3600 * 3)
    return dates_list

# takes a list of locations as strings and returns a list of [state, count]
def count_by_state(invalidate=False):
    if not invalidate:
        graph_data = get_graph_data(keys.RMV_USER_STATES)
        if graph_data: return graph_data

    items = accounts_models.User.active.values_list('location', flat=True)
    states_list = []
    items_list = []
    for x in items:
        try:
            items_list.append(str(x.split(', ')[-1]))
        except UnicodeEncodeError: continue
    counts = collections.Counter(items_list)
    map(lambda x: states_list.append([x, counts[x]]), list(counts))
    set_graph_data(keys.RMV_USER_STATES, states_list, 3600 * 3)
    return states_list

# takes a list of tuples (date, reward) and returns a list of [date, sum]
def sum_by_date(invalidate=False):
    if not invalidate:
        graph_data = get_graph_data(keys.RMV_RATING_SUMS)
        if graph_data: return graph_data

    items = videos_models.Rating.active.values_list('created_date', 'video__reward')
    dates_dict = { }
    for pair in items:
        adj_date = pair[0] - datetime.timedelta(hours=8) # UTC to PST
        date = datetime.datetime(month=adj_date.month, day=adj_date.day, year=adj_date.year)
        if date not in dates_dict: dates_dict[date] = pair[1]
        else: dates_dict[date] += pair[1]
    sums_list = []
    map(lambda x: sums_list.append(['%s-%s-%s' % (x.month, x.day, x.year),
        float(dates_dict[x])]), sorted(dates_dict.keys()))
    set_graph_data(keys.RMV_RATING_SUMS, sums_list, 3600 * 3)
    return sums_list

# gets the number of unique users that have rated a video per day as a list
def users_by_date(invalidate=False):
    if not invalidate:
        graph_data = get_graph_data(keys.RMV_USERS_DAILY_COUNTS)
        if graph_data: return graph_data

    ratings = videos_models.Rating.active.values_list('created_date', 'user_id')
    dates_dict = { }
    local_tz = pytz.timezone(settings.TIME_ZONE)
    for date, uid in ratings:
        adj_date = local_tz.normalize(date.astimezone(local_tz))
        cdate = datetime.datetime(month=adj_date.month, day=adj_date.day, year=adj_date.year)
        if cdate not in dates_dict: dates_dict[cdate] = [uid]
        else: dates_dict[cdate].append(uid)
    users_counts = []
    map(lambda x: users_counts.append(['%s-%s-%s' % (x.month, x.day, x.year),
        len(set(dates_dict[x]))]), sorted(dates_dict.keys()))
    set_graph_data(keys.RMV_USERS_DAILY_COUNTS, users_counts, 3600)
    return users_counts

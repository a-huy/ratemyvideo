import datetime
from django.utils.timezone import now

def capitalize_name(in_name):
    parts = in_name.strip().split(' ')
    return ' '.join([x[0].upper() + x[1:] for x in parts])

def avg_payout_time(dates):
    if len(dates) == 1: return float('inf')
    total_time = datetime.timedelta(0)
    for argi in xrange(0, len(dates) - 1): total_time += dates[argi] - dates[argi + 1]
    return total_time / (len(dates) - 1)

def time_since_last_payout(dates):
    return now() - dates[0]
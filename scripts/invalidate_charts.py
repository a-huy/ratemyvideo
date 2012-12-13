import utils.djangoenv
import datetime
import base.cache_keys as keys
from django.core.cache import cache
from django.utils.timezone import now

yts = now() - datetime.timedelta(days=1)
yesterday = '%s-%s-%s' % (yts.month, yts.day, yts.year)

cache.delete(keys.RMV_RATING_DATES % yesterday)
cache.delete(keys.RMV_USER_DATES % yesterday)
cache.delete(keys.RMV_USER_STATES % yesterday)

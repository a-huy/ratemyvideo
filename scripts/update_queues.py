import utils.djangoenv
import random
import datetime
import itertools

from django.conf import settings
from django.utils.timezone import now
from django.core.cache import cache
import accounts.models as am
import videos.models as vm
import base.cache_keys as keys
from accounts.lib.invite import is_inside_us

DEFAULT_LIMIT = settings.DEFAULT_VIDEO_QUEUE_LIMIT

def create_entry(user, video, curr_time, bonuses=''):
    new_entry = vm.Queue()
    new_entry.user_id = user.id
    new_entry.video_id = video.id
    new_entry.expire_date = curr_time.replace(hour=8, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
    new_entry.bonuses = bonuses
    return new_entry

accounts = am.User.active.all()
# Query all the open videos
videos = vm.Video.active.exclude(tags__contains='verified')
core_vids = filter(lambda x: x.tags.find('core') != -1, videos)
ratings = vm.Rating.active.all()
curr_time = now()

# Clear the table of any expired videos
vm.Queue.active.filter(expire_date__lt=curr_time).delete()
# Then, grab all the queue items that remain
curr_queue = vm.Queue.active.all()

# Create the queue from a pool of unrated videos
for user in accounts:
    cache.delete(keys.ACC_USER_QUEUE % user.fb_id)
    USER_LIMIT = 30 if user.verified else DEFAULT_LIMIT
    verified_vids = vm.Video.active.filter(tags__contains='verified') if user.verified else []
    ratings_vid_ids = [y.video_id for y in filter(lambda x: x.user_id==user.id, ratings)]
    ratings_vid_ids += [q.video_id for q in filter(lambda x: x.user_id==user.id, curr_queue)]
    pool = filter(lambda x: x.id not in ratings_vid_ids, videos)
    random.shuffle(pool)
    if verified_vids:
        verified_pool = filter(lambda x: x.id not in ratings_vid_ids, verified_vids)
        random.shuffle(verified_pool)
        index = min(len(verified_pool), USER_LIMIT/2)
        pool = verified_pool[:index] + pool[:USER_LIMIT-index]
        random.shuffle(pool)
    if core_vids:
        core_pool = filter(lambda x: x.id not in ratings_vid_ids, core_vids)
        pool_vid_ids = [v.id for v in pool[:USER_LIMIT]]
        for cvid in core_pool:
            if cvid.id not in pool_vid_ids: pool.insert(0, cvid)
    queue = []
    domestic = is_inside_us(user.location)
    bonuses = '' if domestic else 'intl'
    for video in pool[:USER_LIMIT]:
        queue.append(create_entry(user, video, curr_time, bonuses))
    if queue: vm.Queue.objects.bulk_create(queue)


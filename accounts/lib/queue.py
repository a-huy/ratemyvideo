import random
import datetime

from django.utils.timezone import now
from django.conf import settings
from django.core.cache import cache
import base.cache_keys as keys
import accounts.models as accounts_models
import videos.models as videos_models
from accounts.lib.invite import is_inside_us

def update_queue(fb_id, max_vids):
    def create_entry(user, vid, time, bonuses):
        fields = {
            'user_id': user.id,
            'video_id': vid,
            'expire_date': time.replace(hour=8, minute=0, second=0, microsecond=0) + \
                datetime.timedelta(days=1),
            'bonuses': bonuses
        }
        return videos_models.Queue(**fields)
    
    curr_time = now()
    
    # Get user ratings and queue
    user = accounts_models.User.active.get(fb_id=fb_id)
    ratings = videos_models.Rating.active.filter(user=user)
    curr_queue = videos_models.Queue.active.filter(user=user)

    # Get all videos
    all = videos_models.Video.active.all()
    verified = list(all.filter(tags__contains='verified').values_list('id', flat=True))
    cores = list(all.filter(tags__contains='core').values_list('id', flat=True))
    rest = list(all.exclude(tags__contains='verified').values_list('id', flat=True))

    # Determine unrated videos
    cache.delete(keys.ACC_USER_QUEUE % fb_id)
    vid_ids = set(list(ratings.filter(user=user).values_list('video__id', flat=True)) + \
        list(curr_queue.filter(user=user).values_list('video__id', flat=True)))
    pool = [x for x in (rest + (verified if user.verified else [])) if x not in vid_ids]
    random.shuffle(pool)
    bonuses = '' if is_inside_us(user.location) else 'intl'
    queue = []
    for core_id in [x for x in cores if x not in vid_ids]:
        if core_id not in pool[:max_vids]: pool.insert(0, core_id)
    for vid in pool[:max_vids]: queue.append(create_entry(user, vid, curr_time, bonuses))
    if queue: videos_models.Queue.objects.bulk_create(queue)
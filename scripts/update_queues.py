import utils.djangoenv
import random
import datetime
import itertools

from django.conf import settings
from django.utils.timezone import now
import accounts.models as am
import videos.models as vm

DEFAULT_LIMIT = settings.DEFAULT_VIDEO_QUEUE_LIMIT

def create_entry(user, video, curr_time):
    new_entry = vm.Queue()
    new_entry.user_id = user.id
    new_entry.video_id = video.id
    new_entry.expire_date = curr_time.replace(hour=8, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
    return new_entry

accounts = am.User.active.all()
# Query all the open videos
videos = vm.Video.active.exclude(tags__contains='verified')
ratings = vm.Rating.active.all()
curr_time = now()

# Clear the table of any expired videos
vm.Queue.active.filter(expire_date__lt=curr_time).delete()
# Then, grab all the queue items that remain
curr_queue = vm.Queue.active.all()

# Create the queue from a pool of unrated videos
for user in accounts:
    verified_vids = vm.Video.active.filter(tags__contains='verified') if user.verified else []
    ratings_vid_ids = [y.video_id for y in filter(lambda x: x.user_id==user.id, ratings)]
    ratings_vid_ids += [q.video_id for q in filter(lambda x: x.user_id==user.id, curr_queue)]
    pool = filter(lambda x: x.id not in ratings_vid_ids, videos)
    random.shuffle(pool)
    if verified_vids:
        verified_pool = filter(lambda x: x.id not in ratings_vid_ids, verified_vids)
        random.shuffle(verified_pool)
        index = min(len(verified_pool), DEFAULT_LIMIT/2)
        pool = verified_pool[:index] + pool[:DEFAULT_LIMIT-index]
        random.shuffle(pool)
    queue = []
    for video in pool[:DEFAULT_LIMIT]:
        queue.append(create_entry(user, video, curr_time))
    if queue: vm.Queue.objects.bulk_create(queue)


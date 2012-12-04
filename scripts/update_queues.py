import utils.djangoenv
import random
import datetime

from django.utils.timezone import now
import accounts.models as am
import videos.models as vm

DEFAULT_LIMIT = 40

accounts = am.User.active.all()
videos = vm.Video.active.all()
ratings = vm.Rating.active.all()
curr_time = now()

# Clear the table of any expired videos
vm.Queue.active.filter(expire_date__lt=curr_time).delete()

# Create the queue from a pool of unrated videos
for user in accounts:
    ratings_vid_ids = [y.id for y in filter(lambda x: x.user_id==user.id, ratings)]
    pool = filter(lambda x: x.id not in ratings_vid_ids, videos)
    random.shuffle(pool)
    queue = []
    for video in pool[:DEFAULT_LIMIT]:
        new_entry = vm.Queue()
        new_entry.user_id = user.id
        new_entry.video_id = video.id
        new_entry.expire_date = curr_time.replace(hour=8, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        queue.append(new_entry)
    if queue: vm.Queue.objects.bulk_create(queue)


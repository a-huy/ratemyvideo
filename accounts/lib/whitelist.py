import random
import datetime

import accounts.models as accounts_models
import videos.models as videos_models
from django.conf import settings
from django.utils.timezone import now

# Creates a video queue from a given User object
def create_queue(user):
    curr_time = now()
    videos = list(videos_models.Video.active.all())
    random.shuffle(videos)
    queue = []
    for video in videos[:settings.DEFAULT_VIDEO_QUEUE_LIMIT]:
        new_entry = videos_models.Queue()
        new_entry.user_id = user.id
        new_entry.video_id = video.id
        new_entry.expire_date = curr_time.replace(hour=8, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        queue.append(new_entry)
    if queue: videos_models.Queue.objects.bulk_create(queue)

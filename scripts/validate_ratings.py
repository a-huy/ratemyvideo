import gdata.youtube.service

import utils.djangoenv

from django.conf import settings
import accounts.models as am
import videos.models as vm

users = am.User.active.all()
videos = vm.Video.active.all()
ratings = vm.Rating.active.all().order_by('created_date')
vids_dict = dict(zip([v.id for v in videos], [v.yt_id for v in videos]))

def get_duration(yt_id):
    yt_service = gdata.youtube.service.YouTubeService()
    uri = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2' % yt_id
    try:
        entry = yt_service.GetYouTubeVideoEntry(uri)
        return int(entry.media.duration.seconds)
    except gdata.service.RequestError:
        return None

for user in users:
    if int(user.id) != 20 and int(user.id) != 21: continue
    num_violations = 0
    print 'Checking user %s (%s)...' % (user.fb_id, user.real_name)
    user_ratings = filter(lambda x: x.user_id == user.id, ratings)
    for argi in xrange(1, len(user_ratings)):
        if argi % 10 == 0: print 'Checked %s ratings...' % argi
        duration = get_duration(vids_dict[user_ratings[argi].video_id])
        time_since_last_rating = (user_ratings[argi].created_date - user_ratings[argi - 1].created_date).seconds
        if time_since_last_rating < duration:
            num_violations += 1
    print 'User has %s violations\n' % ('no' if num_violations == 0 else str(num_violations))
    num_violations = 0

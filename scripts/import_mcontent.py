import utils.djangoenv
import itertools
import videos.models as vm

import gdata.youtube.service as gys

usernames = ['mmasurge', 'xfitdaily', 'beingfatsuckschannel', 'watchinsidemykitchen',
             'watchsuperfoods', 'fooddeconstructed', 'watchwellcast', 'recipewars',
             'watchinsidecars']

yt = gys.YouTubeService()

base_uri = 'https://gdata.youtube.com/feeds/api/users/%s/uploads?max-results=50'
total = 0

for show in usernames:
    for argi in itertools.count():
        uri = (base_uri % show) + '&start-index=%d' % (argi * 50 + 1)
        feed = yt.GetYouTubeVideoFeed(uri)
        if not feed.entry: break
        total += len(feed.entry)
        for entry in feed.entry:
            yt_id = entry.id.text.split('/')[-1]
            print entry.title.text + ' | ' + yt_id + ' (' + entry.media.duration.seconds + ')'
    print 'Current Total: %d' % total
    print ''

print total


import utils.djangoenv
import itertools
import videos.models as vm
from decimal import *
import gdata.youtube.service as gys
from django.utils.encoding import smart_text

usernames = ['mmasurge', 'xfitdaily', 'beingfatsuckschannel', 'watchinsidemykitchen',
             'watchsuperfoods', 'fooddeconstructed', 'watchwellcast', 'recipewars',
             'watchinsidecars']
yt = gys.YouTubeService()
vids_ids = [v.yt_id for v in vm.Video.objects.all()]
base_uri = 'https://gdata.youtube.com/feeds/api/users/%s/uploads?max-results=50'
pending = []

for show in usernames:
    for argi in itertools.count():
        uri = (base_uri % show) + '&start-index=%d' % (argi * 50 + 1)
        feed = yt.GetYouTubeVideoFeed(uri)
        if not feed.entry: break
        for entry in feed.entry:
            yt_id = entry.id.text.split('/')[-1].strip()
            if yt_id in vids_ids: continue
            fields = {
                'yt_id': yt_id,
                'duration': int(entry.media.duration.seconds),
                'title': smart_text(entry.title.text),
                'tags': 'verified'
            }
            pending.append(fields)

for argi in xrange(len(pending)):
    pending[argi]['reward'] = round(max(Decimal(pending[argi]['duration']) * Decimal(0.018431594) / 100, .02), 2)
    new_video = vm.Video(**pending[argi])
    pending[argi] = new_video
if pending: vm.Video.objects.bulk_create(pending)

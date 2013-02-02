import utils.djangoenv
import itertools
import getopt
import sys
import videos.models as vm
from decimal import *
import gdata.youtube.service as gys
from django.utils.encoding import smart_text

yt_ids = vm.Video.objects.values_list('yt_id', flat=True)
yt = gys.YouTubeService()
base_uri = 'https://gdata.youtube.com/feeds/api/users/mahalodotcom/uploads?max-results=50'

def get_vids(max_vids=0, get_all=False):
    pending = []
    for argi in itertools.count():
        if argi % 2 == 0: print '*** processed %d videos ***' % (argi * 50)
        uri = '%s&start-index=%d' % (base_uri, argi * 50 + 1)
        feed = yt.GetYouTubeVideoFeed(uri)
        if not feed.entry: return pending
        for entry in feed.entry:
            if (len(pending) >= max_vids) and not get_all: return pending
            yt_id = entry.id.text.split('/')[-1].strip()
            if yt_id in yt_ids: continue
            duration = int(entry.media.duration.seconds)
            if duration < 10: continue
            scaled_reward = min(round((duration * 0.01) ** 2 / 21.6) * 0.01, 0.15)
            if scaled_reward < 0.01: scaled_reward = 0.01
            data = {
                'title': smart_text(entry.title.text),
                'duration': duration,
                'tags': 'verified',
                'yt_id': yt_id,
                'reward': scaled_reward
            }
            new_vid = vm.Video(**data)
            pending.append(new_vid)

if __name__ == '__main__':
    NUM_VIDS = 0
    GET_ALL = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'an:', ['num=', 'all'])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt in ('-n', '--num'):
            try: NUM_VIDS = int(arg)
            except ValueError:
                print '%s is not a valid number' % arg
                sys.exit(1)
        elif opt in ('-a', '--all'):
            GET_ALL = True
    if NUM_VIDS == 0 and not GET_ALL:
        print 'You must specify the number of videos to retrieve'
        sys.exit(1)
    vids = get_vids(NUM_VIDS, GET_ALL)
    if vids: vm.Video.objects.bulk_create(vids)
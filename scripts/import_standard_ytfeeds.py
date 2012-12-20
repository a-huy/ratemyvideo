import utils.djangoenv
import gdata.youtube.service as gys
import itertools
import re
import getopt
import sys
from decimal import *
import videos.models as vm
from django.utils.encoding import smart_text

# *** WARNING ***
# GData has a maximum of 1000 YouTube videos per feed

AVG_AMT_PER_VID = 5 # cents
NUM_VIDS = 200
MAX_VID_TIME = 900 # seconds (15 minutes)
base_uri = 'https://gdata.youtube.com/feeds/api/standardfeeds/%s&time=today&max-results=50'
all_feeds = ['top_rated', 'top_favorites', 'most_shared', 'most_popular', 'most_recent', 'most_discussed',
         'most_responded', 'recently_featured', 'on_the_web', 'most_viewed']

vid_ids = [v.yt_id for v in vm.Video.objects.all()]

def get_vids(max_time=MAX_VID_TIME, amt_avg=AVG_AMT_PER_VID, feed_names=['most_popular']):
    vids = { }
    yts = gys.YouTubeService()
    if 'all' in feed_names: feed_names = all_feeds

    for type in feed_names:
        uri = (base_uri % type)
        feed = yts.GetYouTubeVideoFeed(uri)

        for vid in feed.entry:
            try:
                # Get the length of the video and perform validation
                duration = int(vid.media.duration.seconds)
                if duration > max_time: continue

                # Get the YouTube ID and perform validation
                yt_id = vid.id.text.split('/')[-1].strip()
                if yt_id in vid_ids: continue
                # Duplicate videos may show up in different queries
                if yt_id in vids: continue

                # Get the other fields
                title = vid.title.text
            except AttributeError: continue

            # Insert the video into the dict
            data = {
                'title': smart_text(title),
                'duration': duration,
                'tags': '',
                'yt_id': yt_id
            }
            vids[yt_id] = data
    return assign_rewards(vids, amt_avg)

def assign_rewards(vids, amt_avg=AVG_AMT_PER_VID):
    total_amt = len(vids) * amt_avg
    total_time = sum([vids[vid]['duration'] for vid in vids])
    getcontext() # Get context for the decimal class
    for vid in vids:
        vids[vid]['reward'] = round(Decimal(vids[vid]['duration']) / Decimal(total_time) * total_amt) / 100
        if vids[vid]['reward'] == 0.0: vids[vid]['reward'] = 0.01
    total_rewards = sum([vids[vid]['reward'] for vid in vids])
    return vids

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'a:f:n:t:', ['average=', 'feed=', 'time='])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(1)
    arg_dict = { }
    feed_names = []
    for opt, arg, in opts:
        if opt in ('-a', '--average'):
            arg_dict['amt_avg'] = int(arg)
        elif opt in ('-t', '--time'):
            arg_dict['max_time'] = int(arg)
        elif opt in ('-f', '--feed'):
            feed_names.append(arg)
    if feed_names: arg_dict['feed_names'] = feed_names

    vids = get_vids(**arg_dict)
    for key in vids.keys():
        new_vid = vm.Video(**vids[key])
        vids[key] = new_vid
    if vids: vm.Video.objects.bulk_create(vids.values())


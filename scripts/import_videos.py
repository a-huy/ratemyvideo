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

vid_ids = [v.yt_id for v in vm.Video.objects.all()]

def get_vids(num_vids=NUM_VIDS, max_time=MAX_VID_TIME, amt_avg=AVG_AMT_PER_VID):
    vids = { }
    yts = gys.YouTubeService()

    for argi in itertools.count():
        query = gys.YouTubeVideoQuery()
        query.max_results = '50'
        query.start_index = argi * 50 + 1
        feed = yts.YouTubeQuery(query)

        for vid in feed.entry:
            # If we have enough videos, start assigning rewards
            if len(vids) == num_vids: return assign_rewards(vids, amt_avg)

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

            # Insert the video into the dict
            vids[yt_id] = {
                'title': smart_text(title),
                'duration': duration,
                'tags': '',
                'yt_id': yt_id
            }

def assign_rewards(vids, amt_avg=AVG_AMT_PER_VID):
    total_amt = len(vids) * amt_avg
    total_time = sum([vids[vid]['duration'] for vid in vids])
    getcontext() # Get context for the decimal class
    for vid in vids:
        vids[vid]['reward'] = round(Decimal(vids[vid]['duration']) / Decimal(total_time) * total_amt) / 100
    total_rewards = sum([vids[vid]['reward'] for vid in vids])
    return vids

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'a:n:t:', ['average=', 'number=', 'time='])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(1)
    arg_dict = { }
    for opt, arg, in opts:
        if opt in ('-a', '--average'):
            arg_dict['amt_avg'] = int(arg)
        elif opt in ('-n', '--number'):
            arg_dict['num_vids'] = int(arg)
        elif opt in ('-t', '--time'):
            arg_dict['max_time'] = int(arg)

    vids = get_vids(**arg_dict)
    for key in vids.keys():
        new_vid = vm.Video(**vids[key])
        vids[key] = new_vid
    if vids: vm.Video.objects.bulk_create(vids.values())


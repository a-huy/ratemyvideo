import gdata.youtube.service
import utils.djangoenv

import videos.models as vm

videos = vm.Video.objects.filter(duration=0)

def get_duration(yt_id):
    yt_service = gdata.youtube.service.YouTubeService()
    uri = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2' % yt_id
    try:
        entry = yt_service.GetYouTubeVideoEntry(uri)
        return int(entry.media.duration.seconds)
    except gdata.service.RequestError:
        return None

dry_run = True

if raw_input('Dry Run? (Y|n): ') == 'n': dry_run = False

print 'Numer of pending updates: %d' % len(videos)

for argi in xrange(len(videos)):
    if argi % 10 == 0: print 'Processed %d videos' % argi
    duration = get_duration(videos[argi].yt_id)
    if not dry_run:
        videos[argi].duration = duration
        videos[argi].save()

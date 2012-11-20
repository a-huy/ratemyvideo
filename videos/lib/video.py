import gdata.youtube.service

# Query gdata for a video title with a given YouTube ID
def get_title_from_yt_id(yt_id):
    yt_service = gdata.youtube.service.YouTubeService()
    uri = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2' % yt_id
    try:
        entry = yt_service.GetYouTubeVideoEntry(uri)
        return entry.title.text
    except gdata.service.RequestError:
        return None


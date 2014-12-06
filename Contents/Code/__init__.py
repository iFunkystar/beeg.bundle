THUMB_URL = 'http://cdn.anythumb.com/640x360/%s.jpg'
THUMB_URL_ORIG = 'http://cdn.anythumb.com/236x177/%s.jpg'
RE_VIDEO_URL = Regex("'file': '([^']+)'")

####################################################################################################
def NormalizeURL(url):

	return url.split('?')[0].rstrip('/')

####################################################################################################
def MetadataObjectForURL(url):

	html = HTML.ElementFromURL(url)

	title = html.xpath('//title/text()')[0].strip()
	summary = html.xpath('//meta[@name="description"]/@content')[0].rsplit(' - free', 1)[0].strip()
	thumb_1 = THUMB_URL % url.split('/')[-1]
	thumb_2 = THUMB_URL_ORIG % url.split('/')[-1]

	return VideoClipObject(
		title = title,
		summary = summary,
		thumb = Resource.ContentsOfURLWithFallback([thumb_1, thumb_2], fallback='icon-default.jpg'),
		content_rating = 'X'
	)

####################################################################################################
def MediaObjectsForURL(url):

	return [
		MediaObject(
			container = Container.MP4,
			video_codec = VideoCodec.H264,
			video_resolution = '480',
			audio_codec = AudioCodec.AAC,
			audio_channels = 2,
			optimized_for_streaming = True if Client.Product not in ['Plex Web'] else False,
			parts = [
				PartObject(
					key = Callback(PlayVideo, url=url)
				)
			]
		)
	]

####################################################################################################
@indirect
def PlayVideo(url):

	data = HTTP.Request(url).content
	video = RE_VIDEO_URL.search(data)

	if video:
		return IndirectResponse(VideoClipObject, key=video.group(1))

	raise Ex.MediaNotAvailable

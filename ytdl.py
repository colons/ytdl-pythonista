#!python3

'''
Directions:

- install youtube-dl via Pip (e.g. using the StaSh command:
  https://github.com/ywangd/stash)
- add this script as a Share extension through Settings -> Share Extension
  Shortcuts
- while watching a video in the YouTube site or app, just share the video to
  Pythonista and select this script
- the video will download, and when it's done you can share the video file
  itself with any app (e.g. VLC) Advanced usage:
- if you specify --stream as the script argument, this script will just grab
  the actual video URL and redirect you to VLC, which will stream the video
  (without interruptions or ads!)

'''

from __future__ import unicode_literals
import youtube_dl
import appex
from objc_util import UIApplication, nsurl

url = appex.get_url()

if url is None:
    text = appex.get_text()
    if 'http' in text:
        url = 'http' + text.split('http', 1)[1]

print("URL: ", url)

if not url or not url.startswith("http"):
    url = input("No URL found - enter URL to download: ")

with youtube_dl.YoutubeDL() as ydl:
    selector = ydl.build_format_selector('best[ext=mp4][height<=?1080]')

    info = ydl.extract_info(url, download=False)
    if info.get('_type') == 'playlist':
        raise NotImplementedError(f'{url} is a playlist')

    selected_format, = selector({'formats': info['formats']})
    video_url = selected_format['url']
    app = UIApplication.sharedApplication()
    app.openURL_(nsurl(video_url))

appex.finish()

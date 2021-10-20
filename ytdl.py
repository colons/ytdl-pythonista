#!python3

from __future__ import unicode_literals
from yt_dlp import YoutubeDL
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

with YoutubeDL() as ydl:
    selector = ydl.build_format_selector('best[ext=mp4][height<=?720]')

    info = ydl.extract_info(url, download=False)
    if info.get('_type') == 'playlist':
        entries = info['entries']
        if len(entries) != 1:
            raise NotImplementedError(f'{url} is a playlist with {len(entries)} entries')
        info, = entries

    selected_format, = selector({'formats': info['formats']})
    video_url = selected_format['url']
    app = UIApplication.sharedApplication()
    app.openURL_(nsurl(video_url))

appex.finish()

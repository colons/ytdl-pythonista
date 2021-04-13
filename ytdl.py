#!python3

'''
Directions:

    - install youtube-dl via Pip (e.g. using the StaSh command: https://github.com/ywangd/stash)
    - add this script as a Share extension through Settings -> Share Extension Shortcuts
    - while watching a video in the YouTube site or app, just share the video to Pythonista and select this script
    - the video will download, and when it's done you can share the video file itself with any app (e.g. VLC)
Advanced usage:
    - if you specify --stream as the script argument, this script will just grab the actual video URL and redirect you
    to VLC, which will stream the video (without interruptions or ads!)
'''

from __future__ import unicode_literals
import youtube_dl
import appex
import console
import clipboard
import os
import sys
from objc_util import UIApplication, nsurl
from urllib.parse import urlencode

outdir = os.path.expanduser("~/Documents/Downloads")
try:
    os.mkdir(outdir)
except FileExistsError:
    pass

if appex.get_attachments():
    # e.g. share from YouTube app
    url = appex.get_attachments()[0]
elif appex.get_urls():
    # e.g. share from Safari
    url = appex.get_urls()[0]
elif appex.get_text():
    url = appex.get_text()
elif clipboard.get():
    url = clipboard.get()

print("URL: ", url)
if not url or not url.startswith("http"):
    url = input("No URL found - enter URL to download: ")

ydl_opts = {'outtmpl': os.path.join(outdir, '%(title)s.%(ext)s')}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    selector = ydl.build_format_selector('best[ext=mp4][height<=?1080]')

    info = ydl.extract_info(url, download=False)
    if info.get('_type') == 'playlist':
        raise NotImplementedError(f'{url} is a playlist')

    info['selected_format'], = selector({'formats': info['formats']})

    if sys.argv[1:] == ['--stream']:
        app = UIApplication.sharedApplication()
        params = {'url': info['formats'][-1]['url']}
        # app.openURL_(nsurl('vlc-x-callback://x-callback-url/stream?' + urlencode(params)))
        app.openURL_(nsurl(params['url']))
    else:
        filepath = ydl.prepare_filename(info)
        console.open_in(filepath)

appex.finish()

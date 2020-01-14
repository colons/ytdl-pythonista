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

if sys.argv[1:] == ['--stream']:
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		info = ydl.extract_info(url, download=False)
		from objc_util import UIApplication, nsurl
		from urllib.parse import urlencode
		app = UIApplication.sharedApplication()
		params = urlencode({'url': info['formats'][-1]['url']})
		app.openURL_(nsurl('vlc-x-callback://x-callback-url/stream?' + params))
else:
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		info = ydl.extract_info(url, download=True)
		filepath = ydl.prepare_filename(info)

	console.open_in(filepath)

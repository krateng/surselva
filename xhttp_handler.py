import os
import re

import yt_dlp
from threading import Thread

from serverutil import *
from settings import *



def str_to_bool(inp):
	return (inp.lower() in ("true"))

def handle(k):

	if (k.delete):
		log("Request: Delete Video " + k.delete)
		return delete_video(k.delete)
	if (k.list):
		log("Request: Show Videos")
		return show_videos()
	if (k.add):
		log(f"Request: Add Video {k.add}, Audio: {k.audioonly}")
		return add_video(k.add,str_to_bool(k.audioonly))

	if (k.localisation):
		log("Request: Get Localisation keys")
		return getSettingsDictPrefix("TEXT_")



def show_videos():
	log("Showing videos")

	from server import jinjaenv

	template = jinjaenv.get_template('videolist.html.jinja')

	return template.render(videos=db_list())

def addVideo(id,audioonly):
	log("Video ID to add: " + id)

	if not re.match(r"^[a-zA-Z0-9_\-]+$",id):
		log("Invalid URL")
		return "ERROR_URL"

	#there is no commitment from google to keep video ids at 11, but it's pretty likely to stay that way and I'd like to filter the urls as much as possible so we can do the actual request asynchronously and the user doesn't have to wait
	if (len(id) != 11):
		log("Invalid URL")
		return "ERROR_URL"


	_thread.start_new_thread(getVideoInfo,(id,audioonly))

	return "SUCCESS"

def deleteVideo(id):
	log("Video ID to delete: " + id)

	db_remove(id)

	try:
		os.remove("videos/" + id + ".mp4")
	except:
		log("Video file could not be deleted, adding it back to database to retain integrity")
		addVideo(id)



	return



def getVideoInfo(id,audioonly):
	log("Retrieving Metadata for Video " + id)

	url = "https://youtube.com/watch?v=" + id
	if audioonly:
		options = {
			'format': 'bestaudio/best',
			'postprocessors': [
				{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3'
				}
			]
		}
	else:
		options = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',}
	ydl = yt_dlp.YoutubeDL(options)
	info = ydl.extract_info(url,download=False)
	title = info.get("title","")
	log("Title: " + title)
	size = info.get('filesize',0)
	for f in info.get("requested_formats",[]):
		size += f["filesize"]
	log("Size: " + str(size) + " Bytes")

	db_add(id,title,audioonly,size)

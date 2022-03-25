import os
import re

import yt_dlp
from threading import Thread

import task_handler
from settings import get_settings
import globals
from logger import log



def str_to_bool(inp):
	return (inp.lower() in ("true"))

def handle(k):

	if (k.delete):
		log("XHTTP Request: Delete Video " + k.delete)
		return delete_video(k.delete)
	if (k.list):
		log("XHTTP Request: Show Videos")
		return show_videos()
	if (k.add):
		log(f"XHTTP Request: Add Video {k.add}, Audio: {k.audioonly}")
		return add_video(k.add,str_to_bool(k.audioonly))

	if (k.localisation):
		log("XHTTP Request: Get Localisation keys")
		return get_settings()['localisation']



def show_videos():
	template = globals.jinjaenv.get_template('videolist.html.jinja')
	return template.render(videos=task_handler.list_tasks())

def add_video(id,audioonly):
	if not re.match(r"^[a-zA-Z0-9_\-]+$",id):
		log("Invalid URL")
		return "ERROR_URL"

	#there is no commitment from google to keep video ids at 11, but it's pretty
	# likely to stay that way and I'd like to filter the urls as much as possible
	# so we can do the actual request asynchronously and the user doesn't have to wait
	if (len(id) != 11):
		log("Invalid URL")
		return "ERROR_URL"


	Thread(target=getVideoInfo,args=(id,audioonly)).start()

	return "SUCCESS"

def delete_video(id):
	log("Video ID to delete: " + id)
	task_handler.remove_task(id) # will also take care of file




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

	task_handler.add_task(id,title,audioonly,size)

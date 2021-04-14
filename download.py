from serverutil import *
from settings import *
from bottle import static_file
import re
import youtube_dl
import _thread
import os

def str_to_bool(inp):
	return (inp.lower() in ("true"))

def GET(k):

	if (k.delete):
		log("Request: Delete Video " + k.delete)
		return deleteVideo(k.delete)
	if (k.list):
		log("Request: Show Videos")
		return showVideos()
	if (k.add):
		log("Request: Add Video " + k.add + ", Audio: " + k.audioonly)
		return addVideo(k.add,str_to_bool(k.audioonly))
		
	if (k.localisation):
		log("Request: Get Localisation keys")
		return getSettingsDictPrefix("TEXT_")
	
	
	if (len(k) == 0):
		log("No Request, showing html file...")
		return static_file("index.html",root="")
		
		
		
def showVideos():
	log("Showing videos")
	
	html = ""
	list = db_list()
	for l in list:
		id = l['id']
		title = l['title'].replace("'","").replace('"','').replace("\\","")
		size = str(l['size'])
		loaded = l['loaded']
		complete = (loaded == 100)
		
		
		log("Listing video " + l['id'] + ", title " + l['title'] + ", size " + str(l['size']) + ", loaded to " + str(l['loaded']) + "%")
		if complete:
			html += "<a href='/videos/" + id + ".mp4' download='" + title + ".mp4'><div class='button-small save'>&nbsp;</div></a><a href='/videos/" + id + ".mp4'><div class='button-small watch'>&nbsp;</div></a><div class='button-small delete' onclick='deleteVideo(\"" + id + "\")'>&nbsp;</div>" + title + "<br/>"
		else:
			##103 pixel in total
			TOTAL_PIXEL = 103
			pixel_yes = int(TOTAL_PIXEL * loaded / 100)
			pixel_no = TOTAL_PIXEL - pixel_yes
			html += "<div class='loadingbar-yes' style='width:" + str(pixel_yes) + "px'>&nbsp;</div><div class='loadingbar-no' style='width:" + str(pixel_no) + "px'>&nbsp;</div>" + title + "<br/>"
	
	
	
	return html
	
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
	ydl = youtube_dl.YoutubeDL(options)
	info = ydl.extract_info(url,download=False)
	title = info.get("title","")
	log("Title: " + title)
	size = info.get('filesize',0)
	for f in info.get("requested_formats",[]):
		size += f["filesize"]
	log("Size: " + str(size) + " Bytes")
	
	db_add(id,title,audioonly,size)
	

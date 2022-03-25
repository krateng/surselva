import time
import os

import yt_dlp

import task_handler
from settings import get_settings
import globals
from logger import log


WAIT = 120

def loop():
	time.sleep(2)
	while True:


		log("Downloader requests clearance...")
		speed = request_dl()
		if (speed == 0):
			log(f"Not allowed to download right now, waiting {WAIT} seconds...");
			time.sleep(WAIT)
		else:
			id,audioonly = task_handler.random_task()
			if (id == ""):
				log(f"No videos to download, sleeping for {WAIT} seconds!")
				time.sleep(WAIT)
			else:
				log("Downloading video " + id)
				try:
					download(id,speed,audioonly)
				except:
					log("Error while downloading.")
				# update task list info
				task_handler.check_tasks()



def download(id,speed,audioonly):
	trymp4 = get_settings()['misc']['MP4']
	url = "https://youtube.com/watch?v=" + id
	outfile = os.path.join(globals.data_dir,"videos","%(id)s")

	options = {
		'outtmpl':outfile,
		'ratelimit':speed*1000
	}
	if audioonly:
		options.update({
			'format': 'bestaudio/best',
			'postprocessors': [
				{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3'
				}
			]
		})
	else:
		options.update({
			'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best'

		})

	ydl = yt_dlp.YoutubeDL(options)
	info = ydl.download([url])


def request_dl():
	speeds = {int(k):int(v) for k,v in get_settings()['download_speeds'].items()}
	tm = time.localtime()
	timeofday = tm.tm_hour*60*60 + tm.tm_min*60 + tm.tm_sec

	speed = 0
	#go to the speeds from start to finish
	for t in speeds:
		if (t*60*60 < timeofday):
			# as long as we haven't reached current time, update speed limit
			speed = speeds[t]
		else:
			break

	return speed

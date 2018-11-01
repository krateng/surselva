import time
import _thread
from serverutil import *
from settings import *
import youtube_dl

### in KB
DOWNLOAD_SPEED =  ([-1] * 24)

#BEGIN_DOWNLOADS_HOUR = 1
#END_DOWNLOADS_HOUR = 23

def loop():
	time.sleep(2)
	while True:
		
		log("Getting download speed rules...")
		
		global DOWNLOAD_SPEED
		speeds = getSettingsDictPrefixFull("BANDWIDTH_")

		# just filling in the array with download speeds. only explicit declarations matter, -1 means the same speed is kept
		#this is so we can immediately tell the downloader how long til the next speed change
		for i in speeds:
			DOWNLOAD_SPEED[int(i)] = int(speeds[i])
		
		#DOWNLOAD_SPEED[24] = DOWNLOAD_SPEED[0]
		
		log("Downloader requests clearance...")
		(wait,speed) = requestDL()
		if (speed == 0):
			log("Not allowed to download right now, waiting " + str(wait) + " seconds...");
			time.sleep(wait)
		else:
			id = db_random()
			if (id == ""):
				log("No videos to download, sleeping for an hour!")
				log("(" + str(wait) + "s to next speed change)")
				time.sleep(3600)
			else:
				log("Downloading video " + id)
				try:
					download(id,speed)
				except:
					log("Error while downloading.")



def download(id,speed):
	trymp4 = getSettingBool("MP4")
	url = "https://youtube.com/watch?v=" + id
	if trymp4:
		options = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best','outtmpl':'videos/%(id)s','ratelimit':speed*1000,}
	else:
		options = {'format': 'bestvideo+bestaudio/best','outtmpl':'videos/%(id)s','ratelimit':speed*1000,}
	ydl = youtube_dl.YoutubeDL(options)
	info = ydl.download([url])


def requestDL():
	tm = time.localtime()
	timeofday = tm.tm_hour*60*60 + tm.tm_min*60 + tm.tm_sec
	log("Time of day: " + str(timeofday))
	
	speed = 0
	
	#go to the speeds from start to finish
	for t in range(len(DOWNLOAD_SPEED)):
		if (t*60*60 < timeofday) and (DOWNLOAD_SPEED[t] != -1):
			# as long as we haven't reached current time, update speed limit
			speed = DOWNLOAD_SPEED[t]
			log("Speed set to " + str(speed))
		elif (DOWNLOAD_SPEED[t] != -1):
			# as soon as we're over, we only want to know how long til the next speed limit change and then immediately end it
			waitsec = t*60*60 - timeofday
			return (waitsec,speed)
			
	# if the elif condition has never been reached (no new limit declared after the current time), we simply wait til the end of the day
	waitsec = 24*60*60 - timeofday
	return (waitsec,speed)
			
	
	
	
#	begintime = BEGIN_DOWNLOADS_HOUR * 60 * 60
#	endtime = END_DOWNLOADS_HOUR * 60 * 60
#	if (timeofday < begintime):
#		sec = begintime - timeofday
#		log("Downloader may begin in " + str(sec) + " seconds.")
#		return sec
#		
#	elif (timeofday < endtime):
#		log("Downloader may begin now.")
#		return 0
#	else:
#		sec = begintime + (24*60*60) - timeofday
#		log("Downloader may begin in " + str(sec) + " seconds.")
#		return sec

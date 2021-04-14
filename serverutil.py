VERBOSE_LOGGING = False


import random
import os
import yaml

def logv(string):
	if VERBOSE_LOGGING:
		print(string)
def log(string):
	print(string)


def load():
	try:
		with open("tasks.yml","r") as taskfile: tasks = yaml.safe_load(taskfile)
	except:
		tasks = []
	return tasks
def save(tasks):
	with open("tasks.yml","w") as taskfile:
		yaml.dump(tasks,taskfile)


def db_add(id,title,audioonly,size):
	tasks = load()
	tasks.append({
		"id":id,
		"title":title,
		"audioonly":audioonly,
		"size":size
	})
	save(tasks)

def db_remove(id):
	tasks = load()
	for element in tasks:
		if element['id'] == id:
			tasks.remove(element)
			break # only remove first
	save(tasks)

def db_random():
	tasks = load()
	
	if len(tasks) == 0:
		return "",False

	nextup = random.choice(tasks)
	log("Next ID to download: " + nextup['id'])
	return nextup['id'],nextup['audioonly']

def db_list():

	loadedfilesraw = os.listdir(path="videos/")


	tasks = load()
	for t in tasks:
		currentsize = 0
		loaded = 0
		done = False

		for f in loadedfilesraw:
			logv("Video " + t['id'] + " checking file " + f)
			if (f.split(".")[0] == t['id']):
				if f.split(".")[-1] in ("mp4","mp3"):
					loaded = 100
					done = True
					break
				else:
					currentsize += os.path.getsize("videos/" + f)


		if not done:

			loaded = int(currentsize * 100 / t['size'])
			if (loaded > 99):
				loaded = 99

		t['loaded'] = loaded


	return tasks


def fileDone(id):
	loadedfilesraw = os.listdir(path="videos/")
	for lf in loadedfilesraw:
		if (lf.endswith(".mp4") and lf.split(".")[0] == id) and not "temp" in lf.split("."):
			return True

	return False







def createSettingsFile():

	if not os.path.isfile("settings.ini"):
		log("Settings file not found, creating!")
		open('settings.ini',"w+").close()



def createVideoFile():

	if not os.path.isfile("tasks.yml"):
		log("Video file not found, creating!")
		open('tasks.yml',"w+").close()

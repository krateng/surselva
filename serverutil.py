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

def fileadd(path,string):
	try:
		file = open(path,"a")
		file.write(string)
		x = True
	except:
		x = False
	finally:
		file.close()
		return x


def fileoverwrite(path,lines):
	try:
		file = open(path,"w")
		for l in lines:
			file.write(l)

		x = True
	except:
		x = False
	finally:
		file.close()
		return x


def fileread(path):
	try:
		file = open(path,"r")
		lines = file.readlines()
	except:
		lines = None
	finally:
		file.close()
		return lines

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
		return ""

	nextup = random.choice(tasks)
	log("Next ID to download: " + nextup['id'])
	return nextup['id']

def db_list():

	loadedfilesraw = os.listdir(path="videos/")
#	loadedfiles = []
#	for f in loadedfilesraw:
#		id = f.split(".")[0]
#		size = 0
#		if (f.endswith(".part")):
#			done = False
#			size = os.path.getsize("download/videos/" + f)
#		elif (f.endswith(".mp4")):
#			done = True
#
#		log("Found file: Done: " + str(done) + ", ID: " + id + ", size: " + str(size))
#
#		if (id in l['id'] for l in loadedfiles):
#			l['size'] += size
#
#		else:
#			loadedfiles.append({})
#


	tasks = load()
	for t in tasks:
		currentsize = 0
		loaded = 0
		done = False

		for f in loadedfilesraw:
			logv("Video " + t['id'] + " checking file " + f)
			if (f.split(".")[0] == t['id'] and f.endswith(".mp4")):
				loaded = 100
				done = True
				break
			elif (f.split(".")[0] == t['id']):
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

	if not os.path.isfile("todo"):
		log("Video file not found, creating!")
		open('todo',"w+").close()

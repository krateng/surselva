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
		tasks = {}
	return tasks
def save(tasks):
	with open("tasks.yml","w") as taskfile:
		yaml.dump(tasks,taskfile)

class TaskFile:
	def __open__(self):
		self.tasks = load()
		return self.tasks
	def __close__(self):
		save(self.tasks)





def db_add(id,title,audioonly,size):
	tasks = load()
	tasks[id] = {
		"title":title,
		"audioonly":audioonly,
		"size":size
	}
	save(tasks)

def db_remove(id):
	tasks = load()
	del tasks[id]
	save(tasks)

def db_random():
	tasks = load()

	if len(tasks) == 0:
		return "",False

	nextup_id = random.choice(list(tasks.keys()))
	nextup = tasks[nextup_id]
	log("Next ID to download: " + nextup_id)
	return nextup_id,nextup['audioonly']

def db_list():

	loadedfilesraw = os.listdir(path="videos/")


	tasks = load()
	for id in tasks:
		taskinfo = tasks[id]
		currentsize = 0
		loaded = 0
		done = False

		for f in loadedfilesraw:
			logv("Video " + id + " checking file " + f)
			if (f.split(".")[0] == id):
				if f.split(".")[-1] in ("mp4","mp3"):
					loaded = 100
					done = True
					break
				else:
					currentsize += os.path.getsize("videos/" + f)


		if not done:

			loaded = int(currentsize * 100 / taskinfo['size'])
			if (loaded > 99):
				loaded = 99

		taskinfo['loaded'] = loaded


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

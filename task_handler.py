


import random
import os
import yaml

import globals
from logger import log





class TaskFile:
	def __init__(self):
		self.taskfile = os.path.join(globals.data_dir,"tasks.yml")

	def __enter__(self):
		try:
			with open(self.taskfile,"r") as taskfiledesc:
				self.tasks = yaml.safe_load(taskfiledesc)
			assert self.tasks is not None
		except:
			self.tasks = {}
		return self.tasks
	def __exit__(self,*_):
		with open(self.taskfile,"w") as taskfiledesc:
			yaml.dump(self.tasks,taskfiledesc)





def db_add(id,title,audioonly,size):
	with TaskFile() as tasks:
		tasks[id] = {
			"title":title,
			"audioonly":audioonly,
			"size":size
		}

def db_remove(id):
	with TaskFile() as tasks:
		del tasks[id]

def db_random():
	with TaskFile() as tasks:

		if len(tasks) == 0:
			return "",False

		nextup_id = random.choice(list(tasks.keys()))
		nextup = tasks[nextup_id]
		log("Next ID to download: " + nextup_id)
		return nextup_id,nextup['audioonly']

def db_list():

	videofolder = os.path.join(globals.data_dir,"videos")
	loadedfilesraw = os.listdir(videofolder)

	tasklist = []
	with TaskFile() as tasks:
		for id in tasks:
			taskinfo = tasks[id]
			taskinfo['id'] = id
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
						currentsize += os.path.getsize(os.path.join(videofolder,f))


			if not done:

				loaded = int(currentsize * 100 / taskinfo['size'])
				if (loaded > 99):
					loaded = 99

			taskinfo['loaded'] = loaded

			tasklist.append(taskinfo)


		return tasklist


def fileDone(id):
	videofolder = os.path.join(globals.data_dir,"videos")
	loadedfilesraw = os.listdir(videofolder)

	for lf in loadedfilesraw:
		if (lf.endswith(".mp4") and lf.split(".")[0] == id) and not "temp" in lf.split("."):
			return True

	return False







def createVideoFile():

	if not os.path.isfile("tasks.yml"):
		log("Video file not found, creating!")
		open('tasks.yml',"w+").close()

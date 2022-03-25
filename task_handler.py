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





def add_task(id,title,audioonly,size):
	with TaskFile() as tasks:
		tasks[id] = {
			"title":title,
			"audioonly":audioonly,
			"size":size,
			"done":False
		}

def remove_task(id):
	with TaskFile() as tasks:
		del tasks[id]

def random_task():
	with TaskFile() as tasks:

		open_tasks = {k:v for k,v in tasks.items() if v['done'] is False}

		if len(open_tasks) == 0:
			return "",False

		nextup_id = random.choice(list(open_tasks.keys()))
		nextup = tasks[nextup_id]
		log("Next ID to download: " + nextup_id)
		return nextup_id,nextup['audioonly']

def check_tasks():
	# updates whether dl is done
	with TaskFile() as tasks:

		videofolder = os.path.join(globals.data_dir,"videos")
		loadedfilesraw = os.listdir(videofolder)

		for f in loadedfilesraw:
			id = f.split(".")[0]
			if id in tasks:
				if f.split(".")[-1] in ("mp4","mp3"):
					tasks[id]['done'] = True
					tasks[id]['ext'] = f.split(".")[-1]


def list_tasks():

	check_tasks()

	videofolder = os.path.join(globals.data_dir,"videos")
	loadedfilesraw = os.listdir(videofolder)

	with TaskFile() as tasks:
		task_view = tasks

	for id in task_view:
		taskinfo = task_view[id]
		taskinfo['id'] = id
		currentsize = 0
		loaded = 0

		if taskinfo['done']:
			loaded = 100
		else:
			for f in loadedfilesraw:
				if (f.split(".")[0] == id):
					currentsize += os.path.getsize(os.path.join(videofolder,f))
					break
			loaded = int(currentsize * 100 / taskinfo['size'])
			if (loaded > 99):
				loaded = 99

		taskinfo['loaded'] = loaded


	return task_view


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

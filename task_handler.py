import random
import os
import yaml

import globals
from logger import log




class TaskFile:
	def __init__(self):
		self.taskfile = globals.user_files['TASKFILE']

	def __enter__(self):
		try:
			with open(self.taskfile,"r") as taskfiledesc:
				self.tasks = yaml.safe_load(taskfiledesc)
			assert self.tasks is not None
		except:
			self.tasks = {}
		return self.tasks
	def __exit__(self,*_):
		with open(self.taskfile,"w+") as taskfiledesc:
			yaml.dump(self.tasks,taskfiledesc)

with TaskFile():
	pass
	# create empty




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
		taskinfo = tasks[id]
		filename = f"{id}.{taskinfo['ext']}"
		log(f"Remove video file {filename}")
		os.remove(os.path.join(globals.user_folders['VIDEOFOLDER'],filename))
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

	with TaskFile() as tasks:

		loadedfilesraw = os.listdir(globals.user_folders['VIDEOFOLDER'])


		for f in loadedfilesraw:
			fullpath = os.path.join(globals.user_folders['VIDEOFOLDER'],f)
			id = f.split(".")[0]
			if id in tasks:
				# updates whether dl is done
				if f.split(".")[-1] in ("mp4","mp3"):
					tasks[id]['done'] = True
					tasks[id]['ext'] = f.split(".")[-1]

			else:
				# deletes unassociated videos
				log(f"Video {f} is orphaned, deleting...")
				os.remove(fullpath)


def list_tasks():

	check_tasks()

	loadedfilesraw = os.listdir(globals.user_folders['VIDEOFOLDER'])

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
					currentsize += os.path.getsize(os.path.join(globals.user_folders['VIDEOFOLDER'],f))
					break
			loaded = int(currentsize * 100 / taskinfo['size'])
			if (loaded > 99):
				loaded = 99

		taskinfo['loaded'] = loaded


	return task_view

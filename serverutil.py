VERBOSE_LOGGING = False


import random
import os

def logv(string):
	if VERBOSE_LOGGING:
		print(string)
def log(string):
	print(string)	
		
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
		
def db_add(id,title,size):
	st = id + "\t" + title + "\t" + str(size) + "\n"
	fileadd("todo",st)
	
def db_remove(id):
	lines = fileread("todo")
	linestoretain = []
	for l in lines:
		if not l.startswith(id):
			linestoretain.append(l)
			
	fileoverwrite("todo",linestoretain)
	
def db_random():
	lines = fileread("todo")
	if (len(lines) == 0):
		return ""
	ids = []	
	for l in lines:
		id = l.split("\t")[0]
		if not fileDone(id):
			ids.append(id)
			
	
	if (len(ids) == 0):
		return ""
	
	nextup = random.choice(ids)
	log("Next ID to download: " + nextup)
	return nextup
	
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
			

	lines = fileread("todo")
	list = []
	for l in lines:
		data = l.split("\t")
		id = data[0]
		title = data[1]
		size = int(data[2])
		currentsize = 0
		loaded = 0
		done = False
		
		for f in loadedfilesraw:
			logv("Video " + id + " checking file " + f)
			if (f.split(".")[0] == id and f.endswith(".mp4")):
				loaded = 100
				done = True
				break
			elif (f.split(".")[0] == id):
				
				
				currentsize += os.path.getsize("videos/" + f)
				
		
		if not done:
					
			
			loaded = int(currentsize * 100 / size)
			if (loaded > 99):
				loaded = 99
			
		
		list.append({'id':id,'title':title,'size':size,'loaded':loaded})
		
		
	
	
		
	return list
	
	
def fileDone(id):
	loadedfilesraw = os.listdir(path="videos/")
	for lf in loadedfilesraw:
		if (lf.endswith(".mp4") and lf.split(".")[0] == id):
			return True
	
	return False
	


def getSettingBool(akey):

	createSettingsFile()


	file = open("settings.ini")
	lines = file.readlines()
	for l in lines:
		l = l.replace("\n","")
		l = l.split("#")[0].split("//")[0]
		if (not l.startswith("//") and not l.startswith("[") and not l.startswith("#") and ("=" in l)):
			
			
			#(key,val) = re.sub(r"(.*)\s+=\s+\"(.*)\"",r"\1,\2",l).split(",")
			(key,val) = l.split("=")
			key = key.strip()
			val = val.strip()
		
		
			if (key == akey):
				if (val in ["True","true",1,"yes"]):
					return True
				else:
					return False
					
	file = open("settings_default.ini")
	lines = file.readlines()
	for l in lines:
		l = l.replace("\n","")
		l = l.split("#")[0].split("//")[0]
		if (not l.startswith("//") and not l.startswith("[") and not l.startswith("#") and ("=" in l)):
			
			
			#(key,val) = re.sub(r"(.*)\s+=\s+\"(.*)\"",r"\1,\2",l).split(",")
			(key,val) = l.split("=")
			key = key.strip()
			val = val.strip()
		
		
			if (key == akey):
				if (val in ["True","true",1,"yes"]):
					return True
				else:
					return False
			
	return False
	
	
def getSettings(*keys):

	createSettingsFile()

	allsettings = {}	
	
	file = open("settings_default.ini")
	lines = file.readlines()
	for l in lines:
		l = l.replace("\n","")
		l = l.split("#")[0].split("//")[0]
		if (not l.startswith("//") and not l.startswith("[") and not l.startswith("#") and ("=" in l)):
			
			
			#(key,val) = re.sub(r"(.*)\s+=\s+\"(.*)\"",r"\1,\2",l).split(",")
			(key,val) = l.split("=")
			key = key.strip()
			val = val.strip()
		
		
			allsettings[key] = val
	
	file = open("settings.ini")
	lines = file.readlines()
	for l in lines:
		l = l.replace("\n","")
		l = l.split("#")[0].split("//")[0]
		if (not l.startswith("//") and not l.startswith("[") and not l.startswith("#") and ("=" in l)):
			
			
			#(key,val) = re.sub(r"(.*)\s+=\s+\"(.*)\"",r"\1,\2",l).split(",")
			(key,val) = l.split("=")
			key = key.strip()
			val = val.strip()
		
		
			allsettings[key] = val
			
	return [allsettings[k] for k in keys]


def getSettingsDict(*keys):

	createSettingsFile()

	settings = {}

	file = open("settings_default.ini")
	lines = file.readlines()
	for l in lines:
		l = l.replace("\n","")
		l = l.split("#")[0].split("//")[0]
		if (not l.startswith("//") and not l.startswith("[") and not l.startswith("#") and ("=" in l)):
			
			
			#(key,val) = re.sub(r"(.*)\s+=\s+\"(.*)\"",r"\1,\2",l).split(",")
			(key,val) = l.split("=")
			key = key.strip()
			val = val.strip()
		
			if (key in keys):
				settings[key] = val
			

	file = open("settings.ini")
	lines = file.readlines()
	for l in lines:
		l = l.replace("\n","")
		l = l.split("#")[0].split("//")[0]
		if (not l.startswith("//") and not l.startswith("[") and not l.startswith("#") and ("=" in l)):
			
			
			#(key,val) = re.sub(r"(.*)\s+=\s+\"(.*)\"",r"\1,\2",l).split(",")
			(key,val) = l.split("=")
			key = key.strip()
			val = val.strip()
		
			if (key in keys):
				settings[key] = val
			
	return settings
	
	
def getSettingsDictPrefix(prefix):

	createSettingsFile()

	settings = {}
	
	file = open("settings_default.ini")
	lines = file.readlines()
	for l in lines:
		l = l.replace("\n","")
		l = l.split("#")[0].split("//")[0]
		if (not l.startswith("//") and not l.startswith("[") and not l.startswith("#") and ("=" in l)):
			
			
			#(key,val) = re.sub(r"(.*)\s+=\s+\"(.*)\"",r"\1,\2",l).split(",")
			(key,val) = l.split("=")
			key = key.strip()
			val = val.strip()
		
			if (key.startswith(prefix)):
				settings[key[len(prefix):]] = val
	
	file = open("settings.ini")
	lines = file.readlines()
	for l in lines:
		l = l.replace("\n","")
		l = l.split("#")[0].split("//")[0]
		if (not l.startswith("//") and not l.startswith("[") and not l.startswith("#") and ("=" in l)):
			
			
			#(key,val) = re.sub(r"(.*)\s+=\s+\"(.*)\"",r"\1,\2",l).split(",")
			(key,val) = l.split("=")
			key = key.strip()
			val = val.strip()
		
			if (key.startswith(prefix)):
				settings[key[len(prefix):]] = val
			
	return settings
	
	
	
def createSettingsFile():

	if not os.path.isfile("settings.ini"):
		log("Settings file not found, creating!")	
		open('settings.ini',"w+").close()
	
	
	
def createVideoFile():

	if not os.path.isfile("todo"):
		log("Video file not found, creating!")	
		open('todo',"w+").close()
	

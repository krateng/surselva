import os
import yaml
import toml

from serverutil import *
import globals

settingsfile = os.path.join(globals.data_dir,"settings.ini")
defaultfile = os.path.join(globals.data_dir,"settings_default.ini")


with open(defaultfile) as dfd:
	try:
		settings = toml.load(dfd)
	except:
		settings = {}
with open(settingsfile) as sfd:
	try:
		settings.update(toml.load(sfd))
	except:
		pass


def get_settings():
	return settings


def getSettingBool(akey):

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


### get settings of one prefix, but don't cherry pick single entries from different settings file - if one entry is defined in settings.ini, ignore all of them in settings_default.ini
def getSettingsDictPrefixFull(prefix):

	settings = {}



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

	if (len(settings) > 0):
		return settings


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

	return settings

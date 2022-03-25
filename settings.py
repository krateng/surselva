import os
import toml

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

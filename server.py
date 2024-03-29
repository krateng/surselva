import os
from threading import Thread
import sys
import random

from bottle import route, run, template, static_file, request, get
import waitress

import globals
from logger import log
from settings import get_settings
import xhttp_handler
import downloader







@get("/videos/<filename>")
def video(filename):
	log("Video file requested: " + filename)
	return static_file(filename,root=os.path.join(globals.data_dir,"videos"))
@get("/backgrounds/<filename>")
def backgrounds(filename):
	return static_file(filename,root=os.path.join(globals.data_dir,"backgrounds"))


@get("/<pth:path>")
def static(pth):
	#log("Static file requested: " + pth)
	return static_file(pth,root="./static")

@route("/xhttp")
def xhttp():
	keys = request.query
	return xhttp_handler.handle(keys)


@get("")
@get("/")
def mainpage():
	keys = request.query
	page_template = globals.jinjaenv.get_template('page.html.jinja')
	log("Requesting main page")
	localisation = get_settings()['localisation']
	try:
		background = random.choice(os.listdir(globals.user_folders['BACKGROUNDFOLDER']))
	except:
		background = ''
	return page_template.render({
		'localisation':localisation,
		'background':background
	})






Thread(target=downloader.loop).start()

host = "0.0.0.0" if "--ipv4" in sys.argv else "::"
port = int(get_settings()['server']['port'])

run(host=host, port=port, server='waitress')

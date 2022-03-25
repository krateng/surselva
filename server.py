import os
from threading import Thread
import json
import sys

from bottle import route, run, template, static_file, request
import waitress


from logger import log
from settings import get_settings
import xhttp_handler
import downloader
import globals

for idx in range(len(sys.argv)):
	if sys.argv[idx] == "--datadir":
		try:
			globals.data_dir = sys.argv[idx+1]
		except:
			raise




@route("/videos/<filename>")
def video(filename):
	log("Video file requested: " + filename)
	return static_file(filename,root=os.path.join(globals.data_dir,"videos"))


@route("/<pth:path>")
def static(pth):
	#log("Static file requested: " + pth)
	return static_file(pth,root="./static")

@route("/xhttp")
def xhttp():
	keys = request.query
	return xhttp_handler.handle(keys)


@route("")
@route("/")
def mainpage():
	keys = request.query
	page_template = globals.jinjaenv.get_template('page.html.jinja')
	log("Requesting main page")
	localisation = get_settings()['localisation']
	return page_template.render({'localisation':localisation,'json':json.dumps(localisation)})






Thread(target=downloader.loop).start()

host = "0.0.0.0" if "--ipv4" in sys.argv else "::"
port = int(get_settings()['server']['port'])

run(host=host, port=port, server='waitress')

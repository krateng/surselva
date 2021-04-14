from bottle import route, run, template, static_file, request
import os
from importlib.machinery import SourceFileLoader
from serverutil import log, db_remove, createVideoFile
import _thread
import waitress
from settings import getSettings, getSettingsDictPrefix
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json


jinjaenv = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
page_template = jinjaenv.get_template('page.html.jinja')


#@route("/<pth:path>/<file:re:.*\\.html>")
#@route("/<pth:path>/<file:re:.*\\.css>")
#@route("/<pth:path>/<file:re:.*\\.js>")
#@route("/<pth:path>/<file:re:.*\\.jpg>")
#@route("/<pth:path>/<file:re:.*\\.png>")
#@route("/<pth:path>/<file:re:.*\\.mp4>")
#@route("/<pth:path>/<file:re:.*\\.mkv>")
@route("/<pth:path>")
def static(pth):
	log("Static file requested: " + pth)
	return static_file(pth,root="")


#@route("/<page>")
#@route("/<page>/")
#def p_download(page):
#	keys = request.query
#	log("Requesting subpage: " + page)
#	return SourceFileLoader(page,page + ".py").load_module().GET(keys)
#@route("/download/")
#def i_download():
#	log("Requesting startpage")
#	return static_file("download/index.html",root="")

@route("")
@route("/")
def mainpage():
	keys = request.query
	log("Requesting main page")
	localisation = getSettingsDictPrefix("TEXT_")
	return page_template.render({'localisation':localisation,'json':json.dumps(localisation)})

@route("/xhttp")
def xhttp():
	keys = request.query
	log("XHTTP Request")
	return SourceFileLoader("download","download.py").load_module().GET(keys)


createVideoFile()

## other programs to always run with the server
_thread.start_new_thread(SourceFileLoader("downloader","downloader.py").load_module().loop,())


port = getSettings("SERVER_PORT")[0]

run(host='::', port=port, server='waitress')

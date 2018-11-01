import re
from serverutil import log
from settings import *

def GET(k):
	
	#default values
#	localisation = {"TEXT_TITLE":"YT Downloader","TEXT_HEADER":"YT Dowloader","TEXT_VIDEO":"Video","TEXT_SUBMIT":"Submit","TEXT_VIDEOLIST":"Videos"}

#	file = open("settings.ini")
#	lines = file.readlines()
#	for l in lines:
#		l = l.replace("\n","")
#		if (not l.startswith("//") and not l.startswith("[") and not l.startswith("#") and ("=" in l)):
#			
#		
#			#(key,val) = re.sub(r"(.*)\s+=\s+\"(.*)\"",r"\1,\2",l).split(",")
#			(key,val) = l.split("=")
#			key = key.strip()
#			val = val.strip()
#		
#		
#			localisation[key] = val
		
	
	localisation = getSettingsDict("TEXT_TITLE","TEXT_HEADER","TEXT_VIDEO","TEXT_SUBMIT","TEXT_VIDEOLIST")	
			
	
	page = """
	
<html>
  <head>
    <title>""" + localisation["TEXT_TITLE"] + """</title>
    <link rel="stylesheet" type="text/css" href="style.css">
    <link rel="icon" type="image/png" href="favicon.png">
    
    <meta charset="utf-8">
    
	<link href="https://fonts.googleapis.com/css?family=Roboto+Mono" rel="stylesheet">
	<link href="https://fonts.googleapis.com/css?family=Pacifico" rel="stylesheet">
	<script type="text/javascript" src="portal.js"></script>
  </head>
  <body onload="pageLoad()">
    <br>
    <h1>""" + localisation["TEXT_HEADER"] + """</h1>

    	<div class="input">""" + localisation["TEXT_VIDEO"] + """: <input class="urlinput" id ="yturl" /> <div class="button" onclick="sendVideo()">""" + localisation["TEXT_SUBMIT"] + """</div></div>
    	
    	<p id="status">&nbsp;</p>
    <br>
    <br>
    <br>
    <br>
    <br>
    
    <div class="category">""" + localisation["TEXT_VIDEOLIST"] + """</div><br/>
    <div class="files" id="filelist">
    	
    </div><br/>
    
    
  

	



  </body>
</html>
	
	
	
	"""


	return page

import re
from serverutil import log
from settings import *
import json


def GET(k):


	localisation = getSettingsDictPrefix("TEXT_")


	page = """

<html>
  <head>
    <title>""" + localisation["TITLE"] + """</title>
    <link rel="stylesheet" type="text/css" href="style.css">
    <link rel="icon" type="image/png" href="favicon.png">

    <meta charset="utf-8">

	<link href="https://fonts.googleapis.com/css?family=Roboto+Mono" rel="stylesheet">
	<link href="https://fonts.googleapis.com/css?family=Pacifico" rel="stylesheet">
	<script type="text/javascript" src="portal.js"></script>

	<script>
		localisation = """ + json.dumps(localisation) + """
	</script>


  </head>
  <body onload="pageLoad()">
    <br>
    <h1>""" + localisation["HEADER"] + """</h1>

    	<div class="input">""" + localisation["VIDEO"] + """: <input class="urlinput" id ="yturl" /> <div class="button" onclick="sendVideo()">""" + localisation["SUBMIT"] + """</div></div>

    	<p id="status">&nbsp;</p>
    <br>
    <br>
    <br>
    <br>
    <br>

    <div class="category">""" + localisation["VIDEOLIST"] + """</div><br/>
    <div class="files" id="filelist">

    </div><br/>



  </body>
</html>



	"""


	return page

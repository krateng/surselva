import sys, os
from jinja2 import Environment, FileSystemLoader, select_autoescape

data_dir = "./data"
for idx in range(len(sys.argv)):
	if sys.argv[idx] == "--datadir":
		data_dir = sys.argv[idx+1]


user_folders = {
	'BACKGROUNDFOLDER': os.path.join(data_dir,"backgrounds"),
	'VIDEOFOLDER': os.path.join(data_dir,"videos")
}
user_files = {
	'TASKFILE': os.path.join(data_dir,"tasks.yml"),
	'SETTINGSFILE': os.path.join(data_dir,"settings.ini"),
}

for fold in user_folders:
	os.makedirs(user_folders[fold],exist_ok=True)



jinjaenv = Environment(
    loader=FileSystemLoader('./jinja'),
    autoescape=select_autoescape(['html', 'xml'])
)

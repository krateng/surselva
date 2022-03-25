import sys, os
from jinja2 import Environment, FileSystemLoader, select_autoescape

data_dir = "./data"
for idx in range(len(sys.argv)):
	if sys.argv[idx] == "--datadir":
		try:
			data_dir = sys.argv[idx+1]
			os.makedirs(data_dir,exist_ok=True)
		except:
			raise




jinjaenv = Environment(
    loader=FileSystemLoader('./jinja'),
    autoescape=select_autoescape(['html', 'xml'])
)

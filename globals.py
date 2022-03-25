from jinja2 import Environment, FileSystemLoader, select_autoescape

data_dir = "./data"


jinjaenv = Environment(
    loader=FileSystemLoader('./jinja'),
    autoescape=select_autoescape(['html', 'xml'])
)

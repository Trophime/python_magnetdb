from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from os import path

from .panels import serving, titles

GLOBAL_CONTEXT = {"version": '0.0.1', "titles": titles}
SECRET_KEY = "CHANGEMEFORTHELOVEOFGOD!!!!!!!!!"
ALLOWED_HOSTS = ["*"]  # Could be made more specific

templates = Jinja2Templates(directory=f"{path.dirname(__file__)}/templates")
static_files = StaticFiles(directory=f"{path.dirname(__file__)}/static")

from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from starlette.background import BackgroundTasks

from ..config import templates
from ..database import engine
from ..models import Material
from ..forms import CFGForm
from ..units import units

import yaml
import json
import os

from python_magnetgeo import Insert, MSite, Bitter, Supra

from python_magnetsetup.config import appenv
from python_magnetsetup.file_utils import MyOpen, search_paths

router = APIRouter()

@router.get("/cfgs.html", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse('cfgs.html', {"request": request})


@router.get("/cfgs", response_class=HTMLResponse)
def index(request: Request):
    print("cfg/index")
    cfgs = {}
    desc = {}
    return templates.TemplateResponse('cfgs/index.html', {
        "request": request, 
        "cfgs": cfgs,
        "descriptions": desc
        })


@router.get("/cfgs/{gname}", response_class=HTMLResponse, name='cfg')
def show(request: Request, gname: str):
    print("cfg/show:", gname)
    MyEnv = appenv()
    
    import os
    print("cfg/show:", os.getcwd())
    geom = gname

    import configparser
    ini_config = configparser.ConfigParser()
    with open(geom, 'r') as cfgdata:
        ini_config.read_string('[DEFAULT]\n[main]\n' + cfgdata.read())

    print("cfg sections:", ini_config.sections())
    print("cfg[DEFAULT]:", ini_config['DEFAULT'])
    print("cfg[main]:", ini_config['main'])
    
    data = dict()
    for section in ini_config.sections():
        print("section:", section)
        data[section] = {}
        for key, val in ini_config.items(section):
            data[section][key] = val
    print("data:", data, type(data))
    
    return templates.TemplateResponse('cfgs/show.html', {"request": request, "cfg": data, "gname": gname})

@router.get("/cfgs/{gname}/edit", response_class=HTMLResponse, name='edit_cfg')
async def edit(request: Request, gname: str):
    print("cfg/edit:", gname)

    import configparser
    ini_config = configparser.ConfigParser()
    with open(gname, 'r') as cfgdata:
        ini_config.read_string('[DEFAULT]\n[main]\n' + cfgdata.read())

    print("cfg sections:", ini_config.sections())
    print("cfg[DEFAULT]:", ini_config['DEFAULT'])
    print("cfg[main]:", ini_config['main'])
    
    data = dict()
    for section in ini_config.sections():
        print("section:", section)
        data[section] = {}
        for key, val in ini_config.items(section):
            data[section][key] = val
    print("data:", data, type(data))

    form = CFGForm(obj=data, request=request)
    return templates.TemplateResponse('cfgs/edit.html', {
        "id": id,
        "request": request,
        "form": form,
    })

@router.post("/cfgs/{gname}/edit", response_class=HTMLResponse, name='update_cfg')
async def update(request: Request, gname: str):
    print("cfg/update:", gname)
    form = await CFGForm.from_formdata(request)
    if form.validate_on_submit():
        return RedirectResponse(router.url_path_for('cfg', gname=gname), status_code=303)
    else:
        return templates.TemplateResponse('cfg/edit.html', {
            "id": id,
            "request": request,
            "form": form,
        })

def remove_file(path: str) -> None:
    os.unlink(path)

@router.get("/cfgs/{gname}/download", response_class=HTMLResponse, name='download_cfg')
async def download(request: Request, gname: str):
    print("cfg/download:", gname)
    
    background_tasks = BackgroundTasks()
    background_tasks.add_task(remove_file, gname)
    return FileResponse(path=gname, filename=gname, background=background_tasks)

@router.get("/cfgs/{gname}/remove", response_class=HTMLResponse, name='remove_cfg')
async def remove(request: Request, gname: str):
    print("cfg/remove:", gname)
    
    background_tasks = BackgroundTasks()
    background_tasks.add_task(remove_file, gname)
    return FileResponse(background=background_tasks)


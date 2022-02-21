from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse

from ..config import templates
from ..database import engine
from ..models import Material
from ..forms import GeomForm
from ..units import units

import yaml
import json

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
    with open(geom, 'r') as cfgdata:
        ini_data = yaml.load(cfgdata, Loader = yaml.FullLoader)
    print("cfg:", ini_data)
    data = json.loads(ini_data.to_json())
    print("data:", data, type(data))
    
    return templates.TemplateResponse('cfgs/show.html', {"request": request, "geom": data, "gname": gname})

@router.get("/cfgs/{gname}/edit", response_class=HTMLResponse, name='edit_cfg')
async def edit(request: Request, gname: str):
    print("cfg/edit:", gname)
    # TODO load cfg from filename==name
    MyEnv = appenv()
    
    import json
    # from python_magnetgeo import Helix
    geom = gname + ".yaml"
    with MyOpen(geom, 'r', paths=search_paths(MyEnv, "geom")) as cfgdata:
        geom = yaml.load(cfgdata, Loader = yaml.FullLoader)
    form = GeomForm(obj=geom, request=request)
    return templates.TemplateResponse('cfgs/edit.html', {
        "id": id,
        "request": request,
        "form": form,
    })

@router.post("/cfgs/{gname}/edit", response_class=HTMLResponse, name='update_cfg')
async def update(request: Request, gname: str):
    print("cfg/update:", gname)
    form = await GeomForm.from_formdata(request)
    if form.validate_on_submit():
        return RedirectResponse(router.url_path_for('cfg', gname=gname), status_code=303)
    else:
        return templates.TemplateResponse('cfg/edit.html', {
            "id": id,
            "request": request,
            "form": form,
        })

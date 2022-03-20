from python_magnetsetup.file_utils import MyOpen, findfile, search_paths
from python_magnetsetup.config import appenv

from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse

from ..config import templates
from ..database import engine
from ..models import Material
from ..forms import GeomForm
from ..units import units

import yaml

from python_magnetgeo import Insert, MSite, Bitter, Supra

router = APIRouter()

@router.get("/cfgs.html", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse('cfgs.html', {"request": request})


@router.get("/cfgs", response_class=HTMLResponse)
def index(request: Request):
    print("geom/index")
    cfgs = {}
    desc = {}
    return templates.TemplateResponse('cfgs/index.html', {
        "request": request, 
        "cfgs": cfgs,
        "descriptions": desc
        })


@router.get("/cfgs/{gname}", response_class=HTMLResponse)
def show(request: Request, gname: str):
    print("cfg/show:", gname)
    # TODO where to get name filename
    # # load yaml file into data
    import os
    print("geom/show:", os.getcwd())

    MyEnv = appenv()
    
    with MyOpen(gname + ".yaml", 'r', paths=search_paths(MyEnv, "cfg") ) as cfgdata:
        geom = yaml.load(cfgdata, Loader = yaml.FullLoader)
    print("cfg:", geom)
    
    import json
    data = json.loads(geom.to_json())
    print("data:", data, type(data))
    
    # re-organize data
    data.pop('__classname__')
    if 'materials' in data: data.pop('materials')
    for key in data:
        if isinstance(data[key], dict) and '__classname__' in data[key]:
            data[key].pop('__classname__')
    
    # TODO for Helices discard pitch, replace turns by actual number of turns
    return templates.TemplateResponse('cfgs/show.html', {"request": request, "geom": data, "gname": gname})

@router.get("/cfgs/{gname}/edit", response_class=HTMLResponse, name='edit_geom')
async def edit(request: Request, gname: str):
    print("geom/edit:", gname)
    # TODO load geom from filename==name
    geom = yaml.load(open("data/" + gname + ".yaml", 'r'))
    form = GeomForm(obj=geom, request=request)
    return templates.TemplateResponse('cfgs/edit.html', {
        "id": id,
        "request": request,
        "form": form,
    })

@router.post("/cfgs/{gname}/edit", response_class=HTMLResponse, name='update_geom')
async def update(request: Request, gname: str):
    print("geom/update:", gname)
    form = await GeomForm.from_formdata(request)
    if form.validate_on_submit():
        return RedirectResponse(router.url_path_for('geom', id=id), status_code=303)
    else:
        return templates.TemplateResponse('geom/edit.html', {
            "id": id,
            "request": request,
            "form": form,
        })

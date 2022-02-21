from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse

from ..config import templates
from ..database import engine
from ..models import Material
from ..forms import ModelJsonForm
from ..units import units

import yaml

from python_magnetgeo import Insert, MSite, Bitter, Supra

from python_magnetsetup.config import appenv
from python_magnetsetup.file_utils import MyOpen, search_paths

import json

router = APIRouter()

@router.get("/model_jsons.html", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse('model_jsons.html', {"request": request})


@router.get("/model_jsons", response_class=HTMLResponse)
def index(request: Request):
    print("model_json/index")
    model_jsons = {}
    desc = {}
    return templates.TemplateResponse('model_jsons/index.html', {
        "request": request, 
        "model_jsons": model_jsons,
        "descriptions": desc
        })


@router.get("/model_jsons/{gname}", response_class=HTMLResponse, name='model_json')
def show(request: Request, gname: str):
    print("model_json/show:", gname)
    
    import os
    print("model_json/show:", os.getcwd())

    print("model_json:", gname)
    with open(gname, "r") as jfile:
        data = json.load(jfile)
    print("data:", data, type(data))
    
    return templates.TemplateResponse('model_jsons/show.html', {"request": request, "geom": data, "gname": gname})

@router.get("/model_jsons/{gname}/edit", response_class=HTMLResponse, name='edit_model_json')
async def edit(request: Request, gname: str):
    print("model_json/edit:", gname)
    
    
    data = json.loads(gname)
    form = ModelJsonForm(obj=data, request=request)
    return templates.TemplateResponse('model_jsons/edit.html', {
        "id": id,
        "request": request,
        "form": form,
    })

@router.post("/model_jsons/{gname}/edit", response_class=HTMLResponse, name='update_model_json')
async def update(request: Request, gname: str):
    print("model_json/update:", gname)
    form = await ModelJsonForm.from_formdata(request)
    if form.validate_on_submit():
        return RedirectResponse(router.url_path_for('model_json', gname=gname), status_code=303)
    else:
        return templates.TemplateResponse('model_json/edit.html', {
            "id": id,
            "request": request,
            "form": form,
        })

from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.routing import APIRouter
from sqlmodel import Session, select

from ..config import templates
from ..database import engine
from ..models import Material
from ..forms import MaterialForm

from ..units import units

router = APIRouter()


@router.get("/materials.html", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse('materials.html', {"request": request})


@router.get("/materials", response_class=HTMLResponse)
def index(request: Request):
    with Session(engine) as session:
        statement = select(Material)
        materials = session.exec(statement).all()
        desc = {}
        for mat in materials:
            desc[mat.id] = {"Nuance": mat.nuance, "Rpe": str(mat.Rpe) + " " + units['Rpe']}

    return templates.TemplateResponse('materials/index.html', {
        "request": request,
        "materials": materials,
        "descriptions": desc
    })


@router.get("/materials/{id}", response_class=HTMLResponse, name='material')
def show(request: Request, id: int):
    with Session(engine) as session:
        material = session.get(Material, id)
        data = material.dict()
        data.pop('id', None)
        return templates.TemplateResponse('materials/show.html', {
            "request": request,
            "material": data,
            "unit": units,
            "material_id": id,
        })


@router.get("/materials/{id}/edit", response_class=HTMLResponse, name='edit_material')
async def edit(request: Request, id: int):
    with Session(engine) as session:
        material = session.get(Material, id)
        form = MaterialForm(obj=material, request=request)
        return templates.TemplateResponse('materials/edit.html', {
            "id": id,
            "request": request,
            "form": form,
        })

@router.post("/materials/{id}/edit", response_class=HTMLResponse, name='update_material')
async def update(request: Request, id: int):
    with Session(engine) as session:
        material = session.get(Material, id)
        form = await MaterialForm.from_formdata(request)
        if form.validate_on_submit():
            form.populate_obj(material)
            session.commit()
            session.refresh(material)
            return RedirectResponse(router.url_path_for('material', id=id), status_code=303)
        else:
            return templates.TemplateResponse('materials/edit.html', {
                "id": id,
                "request": request,
                "form": form,
            })

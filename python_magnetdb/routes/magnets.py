from fastapi import Request, Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select

from ..config import templates
from ..database import engine
from ..models import Magnet, MagnetUpdate 
from ..models import MPart, MPartUpdate
from ..models import MSite, MSiteUpdate 
from ..models import MStatus 
from ..forms import MagnetForm
from ..crud import get_magnet_type

router = APIRouter()


@router.get("/magnets.html", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse('magnets.html', {"request": request})


@router.get("/magnets", response_class=HTMLResponse)
def index(request: Request):
    with Session(engine) as session:
        statement = select(Magnet)
        magnets = session.exec(statement).all()
        desc = {}
        for part in magnets:
            result = get_magnet_type(session, part.id)
            desc[part.id] = {"Type": result[0], "Status:": part.status}
            # TODO add to desc: nbr Helices, inner diameter
    return templates.TemplateResponse('magnets/index.html', {
        "request": request, 
        "magnets": magnets,
        "descriptions": desc
        })


@router.get("/magnets/{id}", response_class=HTMLResponse, name='magnet')
def show(request: Request, id: int):
    with Session(engine) as session:
        magnet = session.get(Magnet, id)
        data = magnet.dict()
        data.pop('id', None)
        data["MParts"] = []
        for part in magnet.mparts:
            data["MParts"].append({"name": part.name, "id": part.id})
        return templates.TemplateResponse('magnets/show.html', {"request": request, "magnet": data, "magnet_id": id})

@router.get("/magnets/{id}/edit", response_class=HTMLResponse, name='edit_magnet')
async def edit(request: Request, id: int):
    with Session(engine) as session:
        magnet = session.get(Magnet, id)
        print("magnets/edit: magnet", magnet)
        form = MagnetForm(obj=magnet, request=request)
        print("magnets/edit: form:", form)
        return templates.TemplateResponse('magnets/edit.html', {
            "id": id,
            "request": request,
            "form": form,
        })

@router.post("/magnets/{id}/edit", response_class=HTMLResponse, name='update_magnet')
async def update(request: Request, id: int):
    with Session(engine) as session:
        magnet = session.get(Magnet, id)
        print("magnets/update:", magnet)
        form = await MagnetForm.from_formdata(request)
        if form.validate_on_submit():
            form.populate_obj(magnet)
            session.commit()
            session.refresh(magnet)
            return RedirectResponse(router.url_path_for('magnet', id=id), status_code=303)
        else:
            return templates.TemplateResponse('magnets/edit.html', {
                "id": id,
                "status": MStatus,
                "request": request,
                "form": form,
            })

MSiteUpdate.update_forward_refs()
MagnetUpdate.update_forward_refs()
MPartUpdate.update_forward_refs()
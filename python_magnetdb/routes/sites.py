from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.routing import APIRouter
from sqlmodel import Session, select

from ..config import templates
from ..database import engine
from ..models import Magnet, MagnetUpdate 
from ..models import MSite, MSiteUpdate 
from ..models import MStatus
from ..forms import MSiteForm

router = APIRouter()


@router.get("/msites.html", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse('msites.html', {"request": request})


@router.get("/sites", response_class=HTMLResponse)
def index(request: Request):
    with Session(engine) as session:
        statement = select(MSite)
        msites = session.exec(statement).all()
        desc = {}
        for site in msites:
           desc[site.id] = {"Status:": site.status} 
    return templates.TemplateResponse('sites/index.html', {
        "request": request, 
        "msites": msites,
        "descriptions": desc
        })


@router.get("/sites/{id}", response_class=HTMLResponse, name='site')
def show(request: Request, id: int):
    with Session(engine) as session:
        msite = session.get(MSite, id)
        data = msite.dict()
        print("blueprint:", data)
        data.pop('id', None)
        data["Magnets"] = []
        for magnet in msite.magnets:
            data["Magnets"].append({"name": magnet.name, "id": magnet.id})
        return templates.TemplateResponse('sites/show.html', {"request": request, "msite": data, "msite_id": id})

@router.get("/sites/{id}/edit", response_class=HTMLResponse, name='edit_site')
async def edit(request: Request, id: int):
    with Session(engine) as session:
        msite = session.get(MSite, id)
        print("sites/edit:", msite)
        form = MSiteForm(obj=msite, request=request)
        return templates.TemplateResponse('sites/edit.html', {
            "id": id,
            "request": request,
            "form": form,
        })
@router.post("/sites/{id}/edit", response_class=HTMLResponse, name='update_site')
async def update(request: Request, id: int):
    with Session(engine) as session:
        msite = session.get(MSite, id)
        form = await MSiteForm.from_formdata(request)
        if form.validate_on_submit():
            form.populate_obj(msite)
            session.commit()
            session.refresh(msite)
            return RedirectResponse(router.url_path_for('site', id=id), status_code=303)
        else:
            return templates.TemplateResponse('sites/edit.html', {
                "id": id,
                "status": MStatus,
                "request": request,
                "form": form,
            })
        
MSiteUpdate.update_forward_refs()
MagnetUpdate.update_forward_refs()
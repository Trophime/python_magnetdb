from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select

from ..config import templates
from ..database import engine
from ..models import MPart, Material
from ..models import MagnetUpdate
from ..models import MPartUpdate
from ..forms import MPartForm

router = APIRouter()


@router.get("/mparts.html", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse('mparts.html', {"request": request})


@router.get("/parts", response_class=HTMLResponse)
def index(request: Request):
    print("parts/index")
    with Session(engine) as session:
        statement = select(MPart)
        mparts = session.exec(statement).all()
        desc = {}
        for part in mparts:
            desc[part.id] = {"Type": part.mtype, "Status:": part.status}
    return templates.TemplateResponse('parts/index.html', {
        "request": request, 
        "mparts": mparts,
        "descriptions": desc
        })


@router.get("/parts/{id}", response_class=HTMLResponse, name='part')
def show(request: Request, id: int):
    with Session(engine) as session:
        mpart = session.get(MPart, id)
        print("mpart/show:", mpart)
        data = mpart.dict()
        if not 'magnets' in data:
            data['magnets'] = []
            for magnet in mpart.magnets:
                data['magnets'].append(magnet)
        data.pop('id', None)
        data['Material'] = session.get(Material, mpart.material_id).name
        print("mpart/show:", data)
        print('data[magnets]=', data['magnets'])
        geom = data['geom'].replace(".yaml","")
        # data.pop('material_id', None)
        return templates.TemplateResponse('parts/show.html', {"request": request, "mpart": data, "mpart_id": id, "geom": geom})

@router.get("/parts/{id}/edit", response_class=HTMLResponse, name='edit_part')
async def edit(request: Request, id: int):
    with Session(engine) as session:
        mpart = session.get(MPart, id)
        form = MPartForm(obj=mpart, request=request)
        return templates.TemplateResponse('parts/edit.html', {
            "id": id,
            "request": request,
            "form": form,
        })

@router.post("/parts/{id}/edit", response_class=HTMLResponse, name='update_part')
async def update(request: Request, id: int):
    with Session(engine) as session:
        mpart = session.get(MPart, id)
        form = await MPartForm.from_formdata(request)
        print("update/form:")
        print("form.material_id=", form.material_id)
        print("form.status=", form.status)
        print("form.magnets=", form.magnets)
        print("type(form.magnets)=", type(form.magnets))
        
        if form.validate_on_submit():
            form.populate_obj(mpart)
            session.commit()
            session.refresh(mpart)
            return RedirectResponse(router.url_path_for('part', id=id), status_code=303)
        else:
            return templates.TemplateResponse('parts/edit.html', {
                "id": id,
                "request": request,
                "form": form,
            })

MagnetUpdate.update_forward_refs()
MPartUpdate.update_forward_refs()

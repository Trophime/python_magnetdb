from typing import List, Optional

from fastapi import HTTPException, Request
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from ..config import templates
from ..database import engine
from ..models import MRecord, MSite

from ..queries import query_mrecord_site, query_mrecord_magnet, query_mrecord_part
from ..forms import RecordForm
from ..choices import objchoices

router = APIRouter()


@router.get("/mrecords.html", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse('mrecords.html', {"request": request})


@router.get("/records", response_class=HTMLResponse)
def index(request: Request):
    # print("mrecord index")
    with Session(engine) as session:
        statement = select(MRecord)
        mrecords = session.exec(statement).all()
        desc = {}

        for record in mrecords:
            # print("record:", record)
            data = record.name.split('_')
            msite = session.get(MSite, record.msite_id)
            # print("msite:", msite)
            rtimestamp = record.rtimestamp.strftime("%d/%m/%Y, %H:%M:%S")
            desc[record.id] = { "Housing": data[0], "Site" : msite.name, "date" : rtimestamp} 
    return templates.TemplateResponse('records/index.html', {"request": request, "mrecords": mrecords, "descriptions": desc})

@router.get("/record_query/{mtype}", response_class=HTMLResponse)
async def edit(request: Request, mtype: str, id: Optional[int]=None):
    print("simulations/bmap: mtype=", mtype)
    """
    with Session(engine) as session:
        simu = create_simulation(session, name='tutu', method='cfpdes', model='thelec', geom='Axi', static=True, linear= True)
    """
    form = RecordForm(request=request)
    form.mobject.choices = objchoices(mtype, None)
    print("type:", mtype)
    print("objchoices:", objchoices(mtype, None) )

    return templates.TemplateResponse('record_queries.html', {
        "request": request,
        "form": form,
        "mtype": mtype
    })


@router.post("/records/query/{mtype}", response_class=HTMLResponse, name='record_query')
async def index_by_query(request: Request, mtype: str):
    print("index_by_query")
    form = await RecordForm.from_formdata(request)
    print("index_by_query/record_query:", form.mobject.data, type(form.mobject.data))
    print("index_by_query/record_query: method", form.method.data)

    if form.errors:
        print("errors:", form.errors)

    if form.validate_on_submit():
        id = form.mobject.data

    with Session(engine) as session:
        if mtype == "MSite":
            mrecords = query_mrecord_site(session, id)
        elif mtype == "Magnet":
            mrecords = query_mrecord_magnet(session, id)
        elif mtype == "MPart":
            mrecords = query_mrecord_part(session, id)
        else:
            raise HTTPException(f"index_by_query: {mtype} unsupported type (type should be MSite, Magnet or MPart)")

        desc = {}
        for record in mrecords:
            # print("record:", record)
            data = record.name.split('_')
            msite = session.get(MSite, record.msite_id)
            # print("msite:", msite)
            rtimestamp = record.rtimestamp.strftime("%d/%m/%Y, %H:%M:%S")
            desc[record.id] = { "Housing": data[0], "Site" : msite.name, "date" : rtimestamp}

    return templates.TemplateResponse('records/index.html', {"request": request, "mrecords": mrecords, "descriptions": desc})


@router.get("/records/{id}", response_class=HTMLResponse)
def show(request: Request, id: int=0):
    with Session(engine) as session:
        mrecord = session.get(MRecord, id)
        data = mrecord.dict()
        data.pop('id', None)
        # data.pop('msite_id', None)

        msite = session.get(MSite, mrecord.msite_id)
        desc = { "Housing": mrecord.name.split('_')[0], "Site" : msite.name} 
        return templates.TemplateResponse('records/show.html', {"request": request, "mrecord": data, "mrecord_id": id, "desc": desc})
        # return templates.TemplateResponse('records/show.html', {"request": request, "mrecord": data, "desc": desc})


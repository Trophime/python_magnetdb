from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from ..config import templates
from ..database import engine
from ..models import MRecord, MSite

router = APIRouter()


@router.get("/mrecords.html", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse('mrecords.html', {"request": request})


@router.get("/records", response_class=HTMLResponse)
def index(request: Request):
    print("mrecord index")
    with Session(engine) as session:
        statement = select(MRecord)
        mrecords = session.exec(statement).all()
        desc = {}

        for record in mrecords:
            print("record:", record)
            data = record.name.split('_')
            msite = session.get(MSite, record.msite_id)
            print("msite:", msite)
            rtimestamp = record.rtimestamp.strftime("%d/%m/%Y, %H:%M:%S")
            desc[record.id] = { "Housing": data[0], "Site" : msite.name, "date" : rtimestamp} 
    return templates.TemplateResponse('records/index.html', {"request": request, "mrecords": mrecords, "descriptions": desc})


@router.get("/records/{id}", response_class=HTMLResponse)
def show(request: Request, id: int):
    with Session(engine) as session:
        mrecord = session.get(MRecord, id)
        data = mrecord.dict()
        data.pop('id', None)
        data.pop('msite_id', None)

        msite = session.get(MSite, mrecord.msite_id)
        desc = { "Housing": mrecord.name.split('_')[0], "Site" : msite.name} 
        return templates.TemplateResponse('records/show.html', {"request": request, "mrecord": data, "desc": desc})


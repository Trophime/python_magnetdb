from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from ..config import templates
from ..database import engine
from ..models import MRecord

router = APIRouter()


@router.get("/mrecords.html", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse('mrecords.html', {"request": request})


@router.get("/records", response_class=HTMLResponse)
def index(request: Request):
    with Session(engine) as session:
        statement = select(MRecord)
        mrecords = session.exec(statement).all()
        desc = {}
    return templates.TemplateResponse('records/index.html', {"request": request, "mrecords": mrecords, "descriptions": desc})


@router.get("/records/{id}", response_class=HTMLResponse)
def show(request: Request, id: int):
    with Session(engine) as session:
        mrecord = session.get(MRecord, id)
        data = mrecord.dict()
        data.pop('id', None)
        return templates.TemplateResponse('records/show.html', {"request": request, "mrecord": data})

from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse

from ..config import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
@router.get("/index.html", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@router.get("/api.html", response_class=HTMLResponse)
def api(request: Request):
    return templates.TemplateResponse('api.html', {"request": request})

@router.get("/settings.html", response_class=HTMLResponse)
def settings(request: Request):
    return templates.TemplateResponse('settings.html', {"request": request})


@router.get("/dev.html", response_class=HTMLResponse)
def dev(request: Request):
    return templates.TemplateResponse('dev.html', {"request": request})

@router.get("/submit/{id}", response_class=HTMLResponse, name="submit")
@router.post("/submit/{id}", response_class=HTMLResponse, name="submit")
def submit(request: Request, id: int):
    return
    
@router.get("/view/{id}", response_class=HTMLResponse, name="view")
@router.post("/view/{id}", response_class=HTMLResponse, name="view")
def view(request: Request, id: int):
    return

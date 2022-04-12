from typing import TYPE_CHECKING, List, Optional

from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.routing import APIRouter
from sqlmodel import Session, select

from ..config import templates
from ..database import engine
from ..choices import objchoices

from python_magnetsetup.config import appenv

router = APIRouter()

@router.get("/settings.html", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse('settings.html', {"request": request})

@router.get("/settings", response_class=HTMLResponse)
def index(request: Request):
    MyEnv = appenv()

    desc = {}
    return templates.TemplateResponse('settings/index.html', {
        "request": request, 
        "descriptions": desc
        })

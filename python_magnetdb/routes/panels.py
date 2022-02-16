from typing import List, Optional

import os
import panel as pn

from fastapi import Request, HTTPException
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from ..config import templates, SECRET_KEY, ALLOWED_HOSTS, GLOBAL_CONTEXT
from ..database import engine
from ..models import MRecord, MSite

from bokeh.embed import server_session, server_document
from bokeh.client import pull_session
from bokeh.util.token import generate_session_id
from ..panels import titles, serving
router = APIRouter()
   
@router.get("/{model}/", response_class=HTMLResponse, name='run_panel')
def panel(request: Request, model: str):
    if model not in titles:
        raise HTTPException(status_code=404, detail="Item not found")

    arguments = {"ID": id}
    url = f"http://0.0.0.0:5006/panel/{model}"
    # script = server_document(url=url, arguments=arguments)

    script = server_session(session_id=generate_session_id(SECRET_KEY, signed=True), url=url)
    
    return templates.TemplateResponse('records/panel.html', {
        "request": request,
        "script": script,
        "title": titles[model],
        **GLOBAL_CONTEXT,
    })

pn.serve(
    serving,
    port=5006,
    allow_websocket_origin=ALLOWED_HOSTS,
    address="0.0.0.0",
    show=False,
    sign_sessions=True,
    secret_key=SECRET_KEY,
    generate_session_ids=False,
    num_process=1 if os.name == "nt" else 2,
)

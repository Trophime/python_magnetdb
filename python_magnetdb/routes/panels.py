from distutils.debug import DEBUG
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
from ..crud import *

from bokeh.embed import server_session, server_document
from bokeh.client import pull_session
from bokeh.util.token import generate_session_id
from ..panels import titles, serving

router = APIRouter()
   
# cannot add an extra id argument for unknown reason   (see also show.html in templates/mrecords)  
@router.get("/{model}/", response_class=HTMLResponse, name='run_panel')
def panel(request: Request, model: str, name: Optional[str]=None, site_id: Optional[int]=None):
    if model not in titles:
        raise HTTPException(status_code=404, detail="Item not found")

    bokeh_session_id = generate_session_id(SECRET_KEY, signed=True)
    url = f"http://0.0.0.0:5006/panel/{model}"
    
    if request.query_params: 
        arguments = request.query_params
        if 'site_id' in arguments:
            print('site_id:', site_id)
            with Session(engine) as session:
                objs = get_msiteid_data(session, site_id)
                site_name = objs['name']
                print('site_id:', site_id, site_name)
                request.query_params._dict['site_name'] = site_name
        print("request.query_params._dict=", request.query_params._dict)
        headers = {"Bokeh-Session-Id": generate_session_id(SECRET_KEY, signed=True)}
        script = server_document(url=url, arguments=request.query_params._dict, headers=headers)
    else:
        script = server_session(session_id=bokeh_session_id, url=url)
    
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
    log_level=DEBUG,
)

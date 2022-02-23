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
async def panel(request: Request, model: str, name: Optional[str]=None, mtype: Optional[str]=None, id: Optional[int]=None, mdata: Optional[tuple]=None ):
    print("panels:", request.query_params)
    if model not in titles:
        raise HTTPException(status_code=404, detail="Item not found")

    bokeh_session_id = generate_session_id(SECRET_KEY, signed=True)
    url = f"http://0.0.0.0:5006/panel/{model}"
    
    if not bool(request.query_params):
        if name and mtype and id: 
            if id :
                print('id:', id)
                with Session(engine) as session:
                    if mtype == 'magnet':
                        magnet = session.get(Magnet, id)
                        objs = get_magnetid_data(session, id)
                        request.query_params._dict['id'] = id
                        request.query_params._dict['name'] = magnet.name
                    elif mtype == 'site':
                        msite = session.get(Magnet, id)
                        objs = get_msiteid_data(session, id)
                        request.query_params._dict['id'] = id
                        request.query_params._dict['site_name'] = msite.name
                    else:
                        raise HTTPException(status_code=404, detail=f"/{model}/: unsupported mtype {mtype}")
            if mdata :
                print('mdata:', mdata)
                request.query_params._dict['mdata'] = mdata
            if mtype :
                request.query_params._dict['mtype'] = mtype
            if name :
                request.query_params._dict['name'] = name
    
            print(f"{model}: request.query_params._dict=", request.query_params._dict)
            headers = {"Bokeh-Session-Id": generate_session_id(SECRET_KEY, signed=True)}
            script = server_document(url=url, arguments=request.query_params._dict, headers=headers)
    
        else:
            script = server_session(session_id=bokeh_session_id, url=url)
    else:
        arguments = request.query_params
        print("panels: arguments", arguments)
        if 'id' in arguments :
            print('id:', id)
            with Session(engine) as session:
                if mtype == 'magnet':
                    magnet = session.get(Magnet, id)
                    objs = get_magnetid_data(session, id)
                    request.query_params._dict['id'] = id
                    request.query_params._dict['name'] = magnet.name
                elif mtype == 'site':
                    msite = session.get(Magnet, id)
                    objs = get_msiteid_data(session, id)
                    request.query_params._dict['site_id'] = id
                    request.query_params._dict['site_name'] = msite.name
                else:
                    raise HTTPException(status_code=404, detail=f"/{model}/: unsupported mtype {mtype}")
        if 'mdata' in arguments :
            request.query_params._dict['mdata'] = mdata

        print(f"{model}: request.query_params._dict=", request.query_params._dict)
        headers = {"Bokeh-Session-Id": generate_session_id(SECRET_KEY, signed=True)}
        script = server_document(url=url, arguments=request.query_params._dict, headers=headers)
    
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

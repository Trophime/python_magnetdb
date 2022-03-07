from typing import TYPE_CHECKING, List, Optional

from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.routing import APIRouter
from sqlmodel import Session, select

from ..config import templates
from ..database import engine
from ..models import Magnet, MSite, MRecord, MSimulation 
from ..models import MStatus
from ..forms import SimulationForm, BmapForm
from ..choices import objchoices

from ..crud import create_simulation
from ..crud import get_magnetid_data, get_msiteid_data 

from python_magnetsetup.config import appenv

router = APIRouter()


@router.get("/simulations.html", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse('simulations.html', {"request": request})

@router.get("/simulations", response_class=HTMLResponse)
def index(request: Request):
    with Session(engine) as session:
        statement = select(MSimulation)
        simus = session.exec(statement).all()
        desc = {}
    return templates.TemplateResponse('simulations/index.html', {
        "request": request, 
        "simus": simus,
        "descriptions": desc
        })

@router.get("/simulations/{id}", response_class=HTMLResponse, name='simulation')
def show(request: Request, id: int):
    print("simulations/show:")
    with Session(engine) as session:
        simu = session.get(MSimulation, id)
        data = simu.dict()
        print("blueprint:", data)
        data.pop('id', None)
        return templates.TemplateResponse('simulations/show.html', {"request": request, "simu": data})

@router.get("/sim_setup/{mtype}", response_class=HTMLResponse, name='simsetup')
async def edit(request: Request, mtype: str):
    print("simulations/setup: mtype=", mtype)
    """
    with Session(engine) as session:
        simu = create_simulation(session, name='tutu', method='cfpdes', model='thelec', geom='Axi', static=True, linear= True)
    """
    form = SimulationForm(request=request)
    form.mobject.choices = objchoices(mtype, None)
    print("type:", mtype)
    print("objchoices:", objchoices(mtype, None) )

    return templates.TemplateResponse('sim_setup.html', {
        "request": request,
        "form": form,
        "mtype": mtype
    })

@router.post("/sim_setup/{mtype}", response_class=HTMLResponse, name='do_setup')
async def dosetup(request: Request, mtype: str):
    form = await SimulationForm.from_formdata(request)
    print("simulations/do_setup:", form.mobject.data, type(form.mobject.data))
    print("simulations/do_setup: method", form.method.data)

    stime="transient"
    if form.static.data:
        stime="static"
    # get object from: id=form.mobject.data
    if form.errors:
        print("errors:", form.errors)

    if form.validate_on_submit():
        # TODO call magnetsetup
        print("trying to create cfg and json")
        MyEnv = appenv()
        
        from argparse import Namespace
        args = Namespace(wd="", 
                magnet="",
                msite="",
                method=form.method.data, 
                time=stime, 
                geom=form.geom.data, 
                model=form.model.data, 
                nonlinear=form.linear.data, 
                cooling=form.cooling.data, 
                scale=1.e-3,
                debug=True,verbose=False, 
                )
        print("args:", args)

        if mtype == "Magnet":
            with Session(engine) as session:
                obj = session.get(Magnet, form.mobject.data)
                confdata = get_magnetid_data(session, form.mobject.data)
            args.magnet = obj.name
            jsonfile = args.magnet
        if mtype == "MSite":
            with Session(engine) as session:
                obj = session.get(MSite, form.mobject.data)
                confdata = get_msiteid_data(session, form.mobject.data)
            args.msite = obj.name
            jsonfile = args.msite

        from python_magnetsetup.setup import setup, setup_cmds
        print("shall enter magnetsetup:", jsonfile)
        with Session(engine) as session:
            (cfgfile, jsonfile, xaofile, meshfile, sim_files) = setup(MyEnv, args, confdata, jsonfile, session)
            cmds = setup_cmds(MyEnv, args, cfgfile, jsonfile, xaofile, meshfile)
        print("magnetsetup cmds:", cmds)
        print("cfgfile:", cfgfile)
        print("jsonfile:", jsonfile)

        # add list of files to be archived


        return templates.TemplateResponse('sim_run.html', {
            "request": request,
            "form": form,
            "mtype": mtype,
            "cfgfile": cfgfile,
            "jsonfile": jsonfile,
            "cmds": cmds
        })
        # return RedirectResponse(router.url_path_for('sim_run.html'), status_code=303)
    else:
        return templates.TemplateResponse('sim_setup.html', {
            "request": request,
            "form": form,
            "mtype": mtype
        })
        
@router.get("/bmap_setup/{mtype}", response_class=HTMLResponse, name='bmapsetup')
async def edit(request: Request, mtype: str, id: Optional[int]=None):
    print("simulations/bmap: mtype=", mtype)
    """
    with Session(engine) as session:
        simu = create_simulation(session, name='tutu', method='cfpdes', model='thelec', geom='Axi', static=True, linear= True)
    """
    form = BmapForm(request=request)
    form.mobject.choices = objchoices(mtype, None)
    print("type:", mtype)
    print("objchoices:", objchoices(mtype, None) )

    return templates.TemplateResponse('bmap_setup.html', {
        "request": request,
        "form": form,
        "mtype": mtype
    })

@router.post("/bmap_setup/{mtype}", response_class=HTMLResponse, name='do_bmap')
async def dobmap(request: Request, mtype: str):
    
    form = await BmapForm.from_formdata(request)
    print("bmap/do_bmap:", form.mobject.data, type(form.mobject.data))
    if form.errors:
        print("errors:", form.errors)

    if form.validate_on_submit():
        id = form.mobject.data
        jsonfile = ""
        magnet=""
        msite=""
        if mtype == 'Magnet':
            print("Magnet id=", id)
            with Session(engine) as session:
                magnet = session.get(Magnet, id)
                jsonfile = magnet.name
                confdata = get_magnetid_data(session, id)
        else:
            print("Site id=", id)
            with Session(engine) as session:
                msite = session.get(MSite, id)
                jsonfile = msite.name
                mtype = "site"
                confdata = get_msiteid_data(session, id)

        MyEnv = appenv()
        from python_magnetsetup.ana import setup
        from argparse import Namespace
        args = Namespace(wd="", magnet=magnet,msite=msite,debug=True,verbose=False)
        with Session(engine) as session:
            Mdata = setup(MyEnv, args, confdata, jsonfile, session)
        print(f"{jsonfile} data loaded", Mdata)

        from .panels import rpanel
        print(f"call panels(bmappannel, name={jsonfile} mtype={mtype.lower()}, id={id})")
        return await rpanel(request, 'bmappanel', name=jsonfile, mtype=mtype.lower(), id=id) #, mdata=Mdata)
    else:
        return templates.TemplateResponse('bmap_setup', {
            "request": request,
            "form": form,
            "mtype": mtype
        })

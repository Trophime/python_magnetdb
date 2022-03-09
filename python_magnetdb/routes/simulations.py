from typing import TYPE_CHECKING, List, Optional

from fastapi import Request, HTTPException
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

# comment passer args??
# get: selectmachine(request: Request, server: str, cfgfile: str, jsonfile):
# post: domachine(request: Request, server: str, cfgfile: str, jsonfile):

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
            try:
                (name, cfgfile, jsonfile, xaofile, meshfile, tarfile) = setup(MyEnv, args, confdata, jsonfile, session)
                print("name (yaml):", name)
                print("cfgfile:", cfgfile)
                print("jsonfile:", jsonfile)
                # create cmds
                cmds = setup_cmds(MyEnv, args, name, cfgfile, jsonfile, xaofile, meshfile)
            except ValueError as err:
                raise HTTPException(status_code=404, detail=f"setup of {obj.name} {mtype} failed: {err}")
            except FileExistsError as err:
                raise HTTPException(status_code=404, detail=f"setup of {obj.name} {mtype} failed: {err}")
            except RuntimeError as err:
                raise HTTPException(status_code=404, detail=f"setup of {obj.name} {mtype} failed: {err}")
            except RuntimeError as err:
                raise HTTPException(status_code=404, detail=f"setup of {obj.name} {mtype} failed: {err}")
            except Exception as err:
                raise HTTPException(status_code=404, detail=f"setup of {obj.name} {mtype} failed: {err}")

        print("magnetsetup cmds:", cmds)
        
        machine = MyEnv.compute_server
        print(f"machine={machine}")
        return templates.TemplateResponse('sim_run.html', {
            "request": request,
            "form": form,
            "machine": machine,
            "cfgfile": cfgfile,
            "jsonfile": jsonfile,
            "tarfile": tarfile,
            "name": name,
            "cmds": cmds
        })
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
        return templates.TemplateResponse('bmap_setup.html', {
            "request": request,
            "form": form,
            "mtype": mtype
        })

@router.get("/stressmap_setup/{mtype}", response_class=HTMLResponse, name='stressmapsetup')
async def stressedit(request: Request, mtype: str, id: Optional[int]=None):
    print("simulations/stressmap: mtype=", mtype)
    """
    with Session(engine) as session:
        simu = create_simulation(session, name='tutu', method='cfpdes', model='thelec', geom='Axi', static=True, linear= True)
    """
    form = BmapForm(request=request)
    form.mobject.choices = objchoices(mtype, None)
    print("type:", mtype)
    print("objchoices:", objchoices(mtype, None) )

    return templates.TemplateResponse('stressmap_setup.html', {
        "request": request,
        "form": form,
        "mtype": mtype
    })

@router.post("/stressmap_setup/{mtype}", response_class=HTMLResponse, name='do_stressmap')
async def dostressmap(request: Request, mtype: str):
    
    form = await BmapForm.from_formdata(request)
    print("stressmap/do_stressmap:", form.mobject.data, type(form.mobject.data))
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
        print(f"call panels(stresspannel, name={jsonfile} mtype={mtype.lower()}, id={id})")
        return await rpanel(request, 'stressmappanel', name=jsonfile, mtype=mtype.lower(), id=id) #, mdata=Mdata)
    else:
        return templates.TemplateResponse('stressmap_setup.html', {
            "request": request,
            "form": form,
            "mtype": mtype
        })

@router.get("/self_setup/{mtype}", response_class=HTMLResponse, name='selfsetup')
async def selfedit(request: Request, mtype: str, id: Optional[int]=None):
    print("simulations/self: mtype=", mtype)
    """
    with Session(engine) as session:
        simu = create_simulation(session, name='tutu', method='cfpdes', model='thelec', geom='Axi', static=True, linear= True)
    """
    form = BmapForm(request=request)
    form.mobject.choices = objchoices(mtype, None)
    print("type:", mtype)
    print("objchoices:", objchoices(mtype, None) )

    return templates.TemplateResponse('self_setup.html', {
        "request": request,
        "form": form,
        "mtype": mtype
    })

@router.post("/self_setup/{mtype}", response_class=HTMLResponse, name='do_self')
async def dostressmap(request: Request, mtype: str):
    
    form = await BmapForm.from_formdata(request)
    print("self/do_self:", form.mobject.data, type(form.mobject.data))
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

        raise HTTPException(status_code=404, detail="do_self not implemented")
    else:
        return templates.TemplateResponse('self_setup.html', {
            "request": request,
            "form": form,
            "mtype": mtype
        })


@router.get("/forces_setup/{mtype}", response_class=HTMLResponse, name='forcessetup')
async def forces(request: Request, mtype: str, id: Optional[int]=None):
    print("simulations/self: mtype=", mtype)
    """
    with Session(engine) as session:
        simu = create_simulation(session, name='tutu', method='cfpdes', model='thelec', geom='Axi', static=True, linear= True)
    """
    form = BmapForm(request=request)
    form.mobject.choices = objchoices(mtype, None)
    print("type:", mtype)
    print("objchoices:", objchoices(mtype, None) )

    return templates.TemplateResponse('forces_setup.html', {
        "request": request,
        "form": form,
        "mtype": mtype
    })

@router.post("/forces_setup/{mtype}", response_class=HTMLResponse, name='do_forces')
async def dostressmap(request: Request, mtype: str):
    
    form = await BmapForm.from_formdata(request)
    print("forces/do_forces:", form.mobject.data, type(form.mobject.data))
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

        raise HTTPException(status_code=404, detail="do_forces not implemented")

    else:
        return templates.TemplateResponse('forces_setup.html', {
            "request": request,
            "form": form,
            "mtype": mtype
        })


@router.get("/failures_setup/{mtype}", response_class=HTMLResponse, name='failuressetup')
async def failureedit(request: Request, mtype: str, id: Optional[int]=None):
    print("simulations/failures: mtype=", mtype)
    """
    with Session(engine) as session:
        simu = create_simulation(session, name='tutu', method='cfpdes', model='thelec', geom='Axi', static=True, linear= True)
    """
    form = BmapForm(request=request)
    form.mobject.choices = objchoices(mtype, None)
    print("type:", mtype)
    print("objchoices:", objchoices(mtype, None) )

    return templates.TemplateResponse('failures_setup.html', {
        "request": request,
        "form": form,
        "mtype": mtype
    })

@router.post("/failures_setup/{mtype}", response_class=HTMLResponse, name='do_failures')
async def dostressmap(request: Request, mtype: str):
    
    form = await BmapForm.from_formdata(request)
    print("failures/do_failures:", form.mobject.data, type(form.mobject.data))
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
        raise HTTPException(status_code=404, detail="do_failures not implemented")

    else:
        return templates.TemplateResponse('failures_setup.html', {
            "request": request,
            "form": form,
            "mtype": mtype
        })


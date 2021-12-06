from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.routing import APIRouter
from sqlmodel import Session, select

from ..config import templates
from ..database import engine
from ..models import MSimulation 
from ..models import MStatus
from ..forms import SimulationForm
from ..choices import objchoices

from ..crud import create_simulation

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

@router.get("/sim_setup/{mtype}", response_class=HTMLResponse)
async def edit(request: Request, mtype: str):
    print("simulations/setup: mtype=", mtype)
    """
    with Session(engine) as session:
        simu = create_simulation(session, name='tutu', method='cfpdes', model='thelec', geom='Axi', static=True, linear= True)
    """
    form = SimulationForm(request=request) # SimulationForm.from_formdata(request) # 
    form.mobject.choices = objchoices(mtype, None)
    print("type:", mtype)
    print("objchoices:", objchoices(mtype, None) )

    return templates.TemplateResponse('sim_setup.html', {
        "request": request,
        "form": form,
    })

@router.post("/sim_setup", response_class=HTMLResponse, name='do_setup')
async def do_setup(request: Request):
    print("simulations/do_setup:")
    form = await SimulationForm.from_formdata(request)
    if form.errors:
        print("errors:", form.errors)

    if form.validate_on_submit():
        # TODO call magnetsetup
        cmds = { "mesh":"tut", "sim": "titi"}
        return templates.TemplateResponse('sim_run.html', {
            "request": request,
            "form": form,
            "cmds": cmds
        })
        # return RedirectResponse(router.url_path_for('sim_run.html'), status_code=303)
    else:
        return templates.TemplateResponse('sim_setup', {
            "request": request,
            "form": form,
        })
        

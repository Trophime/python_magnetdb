from typing import Union, List

from fastapi import APIRouter, HTTPException, Depends, Form, Query
from pydantic import BaseModel

from python_magnetsetup.config import loadconfig, supported_methods, supported_models

from ... import worker
from ...actions.generate_simulation_config import generate_simulation_config
from ...actions.get_simulation_measures import get_simulation_measures
from ...dependencies import get_user
from ...models.audit_log import AuditLog
from ...models.magnet import Magnet
from ...models.simulation import Simulation
from ...models.simulation_current import SimulationCurrent
from ...models.site import Site

router = APIRouter()


@router.get("/api/simulations")
def index(user=Depends(get_user('read')), page: int = 1, per_page: int = Query(default=25, lte=100),
          sort_by: str = Query(None), sort_desc: bool = Query(False)):
    simulations = Simulation \
        .with_('resource', 'owner') \
        .order_by(sort_by or 'created_at', 'desc' if sort_desc else 'asc') \
        .paginate(per_page, page)
    items = simulations.serialize()
    for item in items:
        item["owner"] = {"name": item["owner"]["name"]}

    return {
        "current_page": simulations.current_page,
        "last_page": simulations.last_page,
        "total": simulations.total,
        "items": items,
    }


@router.get("/api/simulations/models")
def models():
    app_config = loadconfig()

    available_models = []
    for method in supported_methods(app_config):
        for geometry in ['Axi', '3D']:
            for time in ['static', 'transient']:
                for model in supported_models(app_config, method, geometry, time):
                    available_models.append({
                        "method": method,
                        "geometry": geometry,
                        "time": time,
                        "model": model,
                    })
    return available_models


class CreatePayloadCurrent(BaseModel):
    magnet_id: int
    value: float
    # type: str


class CreatePayload(BaseModel):
    resource_type: str
    resource_id: int
    method: str
    model: str
    geometry: str
    cooling: str
    static: bool
    non_linear: bool
    currents: List[CreatePayloadCurrent]


@router.post("/api/simulations/current")
def create_currents(payload: CreatePayloadCurrent, user=Depends(get_user('create'))):
    #print(f'/api/simulations/currents, {user}: - payload={payload}')

    # can I get magnet type?
    data = Magnet.find(payload.magnet_id)
    print(f'create_currents: magnet={data}') 
    
    # current = CreatePayloadCurrent(
    #     magnet_id=payload.magnet_id, value=payload.value, type=payload.type
    # )
    current = CreatePayloadCurrent(
        magnet_id=payload.magnet_id, value=payload.value
    )
    #print(f'/api/simulations, {user}: current created - payload={payload}')
    return current

@router.post("/api/simulations")
def create(payload: CreatePayload, user=Depends(get_user('create'))):
    #print(f'/api/simulations, {user}: - payload={payload}')
    if payload.resource_type == 'magnet':
        resource = Magnet.find(payload.resource_id)
    elif payload.resource_type == 'site':
        resource = Site.find(payload.resource_id)

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    simulation = Simulation(
        method=payload.method, model=payload.model, geometry=payload.geometry,
        cooling=payload.cooling, static=payload.static, non_linear=payload.non_linear
    )

    # TODO add magnet_type to current 
    currents = map(lambda value: SimulationCurrent(magnet_id=value.magnet_id, value=value.value), payload.currents)
    simulation.owner().associate(user)
    simulation.resource().associate(resource)
    simulation.save()
    simulation.currents().save_many(currents)
    AuditLog.log(user, "Simulation created", resource=simulation)
    return simulation.serialize()


@router.get("/api/simulations/{id}")
def show(id: int, user=Depends(get_user('read'))):
    simulation = Simulation.\
        with_('resource', 'setup_output_attachment', 'output_attachment', 'log_attachment', 'currents.magnet').\
        find(id)
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return simulation.serialize()


@router.delete("/api/simulations/{id}")
def destroy(id: int, user=Depends(get_user('read'))):
    simulation = Simulation.find(id)
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")

    AuditLog.log(user, "Simulation deleted", resource=simulation)
    simulation.delete()
    return simulation.serialize()


@router.get("/api/simulations/{id}/config.json")
def config(id: int, user=Depends(get_user('read'))):
    simulation = Simulation.find(id)
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return generate_simulation_config(simulation)


@router.post("/api/simulations/{id}/run_setup")
def run_setup(id: int, user=Depends(get_user('update'))):
    simulation = Simulation.with_('resource').find(id)
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation.setup_status = "scheduled"
    simulation.save()
    AuditLog.log(user, "Simulation setup scheduled", resource=simulation)
    worker.run_simulation_setup.delay(simulation.id)
    return simulation.serialize()


@router.post("/api/simulations/{id}/run")
def run(id: int, server_id: int = Form(None), cores: int = Form(...), user=Depends(get_user('update'))):
    simulation = Simulation.with_('resource').find(id)
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation.status = "scheduled"
    simulation.save()
    AuditLog.log(user, "Simulation scheduled", resource=simulation)
    worker.run_simulation.delay(simulation.id, server_id, cores)
    return simulation.serialize()


@router.get("/api/simulations/{id}/measures")
def measures(id: int, measure_name: str = Query(None), user=Depends(get_user('read'))):
    measures = get_simulation_measures(id, measure_name)
    if measures is None:
        raise HTTPException(status_code=404, detail="Measures not found")
    return measures

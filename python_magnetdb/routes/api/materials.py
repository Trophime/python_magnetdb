from typing import Optional

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Query, Depends

from ...dependencies import get_user
from ...models.audit_log import AuditLog
from ...models.material import Material

router = APIRouter()


class MaterialPayload(BaseModel):
    name: str
    description: Optional[str]
    nuance: Optional[str]
    t_ref: Optional[float] = 20
    volumic_mass: Optional[float] = 0
    alpha: Optional[float] = 0
    specific_heat: Optional[float] = 0
    electrical_conductivity: Optional[float] = 0
    thermal_conductivity: Optional[float] = 0
    magnet_permeability: Optional[float] = 0
    young: Optional[float] = 0
    poisson: Optional[float] = 0
    expansion_coefficient: Optional[float] = 0
    rpe: float


@router.get("/api/materials")
def index(user=Depends(get_user('read')), page: int = 1, per_page: int = Query(default=25, lte=100),
          query: str = Query(None), sort_by: str = Query(None), sort_desc: bool = Query(False)):
    materials = Material
    if query is not None and query.strip() != '':
        materials = materials.where('name', 'ilike', f'%{query}%')
    if sort_by is not None:
        materials = materials.order_by(sort_by, 'desc' if sort_desc else 'asc')
    materials = materials.paginate(per_page, page)
    return {
        "current_page": materials.current_page,
        "last_page": materials.last_page,
        "total": materials.total,
        "items": materials.serialize(),
    }


@router.post("/api/materials")
def create(payload: MaterialPayload, user=Depends(get_user('create'))):
    material = Material.create(payload.dict(exclude_unset=True))
    AuditLog.log(user, "Material created", resource=material)
    return material.serialize()


@router.get("/api/materials/{id}")
def show(id: int, user=Depends(get_user('read'))):
    material = Material.with_('parts').find(id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material.serialize()


@router.patch("/api/materials/{id}")
def update(id: int, payload: MaterialPayload, user=Depends(get_user('update'))):
    material = Material.find(id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    material.update(payload.dict(exclude_unset=True))
    AuditLog.log(user, "Material updated", resource=material)
    return material.serialize()


@router.delete("/api/materials/{id}")
def destroy(id: int, user=Depends(get_user('delete'))):
    material = Material.find(id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    material.delete()
    AuditLog.log(user, "Material deleted", resource=material)
    return material.serialize()

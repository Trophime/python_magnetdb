from typing import List

import orator
from fastapi import APIRouter, Query, HTTPException, Depends
from fastapi.params import Form

from ...dependencies import get_user
from ...models.audit_log import AuditLog
from ...models.material import Material
from ...models.part import Part

router = APIRouter()


@router.get("/api/parts")
def index(user=Depends(get_user('read')), page: int = 1, per_page: int = Query(default=25, lte=100),
          query: str = Query(None), sort_by: str = Query(None), sort_desc: bool = Query(False),
          status: List[str] = Query(default=None, alias="status[]")):
    parts = Part \
        .order_by(sort_by or 'created_at', 'desc' if sort_desc else 'asc')
    if query is not None and query.strip() != '':
        parts = parts.where('name', 'ilike', f'%{query}%')
    if status is not None:
        parts = parts.where_in('status', status)
    parts = parts.paginate(per_page, page)
    return {
        "current_page": parts.current_page,
        "last_page": parts.last_page,
        "total": parts.total,
        "items": parts.serialize(),
    }


@router.post("/api/parts")
def create(user=Depends(get_user('create')), name: str = Form(...), description: str = Form(None),
           type: str = Form(...), material_id: str = Form(...), design_office_reference: str = Form(None)):
    material = Material.find(material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    part = Part(name=name, description=description, status='in_study', type=type,
                design_office_reference=design_office_reference)
    part.material().associate(material)
    try:
        part.save()
    except orator.exceptions.query.QueryException as e:
        raise HTTPException(status_code=422, detail="Name already taken.") if e.message.find('parts_name_unique') != -1 else e
    AuditLog.log(user, "Part created", resource=part)
    return part.serialize()


@router.get("/api/parts/{id}/sites")
def sites(id: int, user=Depends(get_user('read'))):
    part = Part.with_('magnet_parts.magnet.site_magnets.site').find(id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    result = []
    for magnet_part in part.magnet_parts:
        for site_magnet in magnet_part.magnet.site_magnets:
            result.append(site_magnet.site.serialize())
    return {'sites': result}


@router.get("/api/parts/{id}/records")
def records(id: int, user=Depends(get_user('read'))):
    part = Part.with_('magnet_parts.magnet.site_magnets.site.records').find(id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    result = []
    for magnet_part in part.magnet_parts:
        for site_magnet in magnet_part.magnet.site_magnets:
            for record in site_magnet.site.records:
                result.append(record.serialize())
    return {'records': result}


@router.get("/api/parts/{id}")
def show(id: int, user=Depends(get_user('read'))):
    part = Part.with_('material', 'cad.attachment', 'geometries.attachment', 'magnet_parts.magnet').find(id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    # print(f'part/show: {part.to_dict()}')
    return part.serialize()


@router.patch("/api/parts/{id}")
def update(id: int, user=Depends(get_user('update')), name: str = Form(...), description: str = Form(None),
           type: str = Form(...), material_id: str = Form(...), design_office_reference: str = Form(None)):
    part = Part.with_('material', 'cad.attachment', 'geometries.attachment').find(id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    material = Material.find(material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    part.name = name
    part.description = description
    part.type = type
    part.design_office_reference = design_office_reference
    part.material().associate(material)
    part.save()
    AuditLog.log(user, "Part updated", resource=part)
    return part.serialize()


@router.post("/api/parts/{id}/defunct")
def defunct(id: int, user=Depends(get_user('update'))):
    part = Part.find(id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    part.status = 'defunct'
    part.save()
    AuditLog.log(user, "Part defunct", resource=part)
    return part.serialize()


@router.delete("/api/parts/{id}")
def destroy(id: int, user=Depends(get_user('delete'))):
    part = Part.find(id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    part.delete()
    AuditLog.log(user, "Part deleted", resource=part)
    return part.serialize()

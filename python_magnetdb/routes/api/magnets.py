from datetime import datetime

import orator.exceptions.query
from fastapi import APIRouter, Query, HTTPException, Form, UploadFile, File, Depends

from ...dependencies import get_user
from ...models.attachment import Attachment
from ...models.audit_log import AuditLog
from ...models.magnet import Magnet

router = APIRouter()


@router.get("/api/magnets")
def index(user=Depends(get_user('read')), page: int = 1, per_page: int = Query(default=25, lte=100),
          query: str = Query(None), sort_by: str = Query(None), sort_desc: bool = Query(False)):
    magnets = Magnet
    if query is not None and query.strip() != '':
        magnets = magnets.where('name', 'ilike', f'%{query}%')
    if sort_by is not None:
        magnets = magnets.order_by(sort_by, 'desc' if sort_desc else 'asc')
    magnets = magnets.paginate(per_page, page)
    return {
        "current_page": magnets.current_page,
        "last_page": magnets.last_page,
        "total": magnets.total,
        "items": magnets.serialize(),
    }


@router.post("/api/magnets")
def create(user=Depends(get_user('create')), name: str = Form(...), description: str = Form(None),
           design_office_reference: str = Form(None)):
    magnet = Magnet(name=name, description=description, design_office_reference=design_office_reference,
                    status='in_study')
    try:
        magnet.save()
    except orator.exceptions.query.QueryException as e:
        if e.message.find('magnets_name_unique') != -1:
            raise HTTPException(status_code=422, detail="Name already taken.")
        raise e

    AuditLog.log(user, "Magnet created", resource=magnet)
    return magnet.serialize()


@router.get("/api/magnets/{id}")
def show(id: int, user=Depends(get_user('read'))):
    magnet = Magnet.with_('magnet_parts.part', 'site_magnets.site', 'cad.attachment', 'geometry').find(id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")
    return magnet.serialize()


@router.patch("/api/magnets/{id}")
def update(id: int, user=Depends(get_user('update')), name: str = Form(...), description: str = Form(None),
           design_office_reference: str = Form(None), geometry: UploadFile = File(None)):
    magnet = Magnet.with_('cad.attachment', 'geometry').find(id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")

    magnet.name = name
    magnet.description = description
    magnet.design_office_reference = design_office_reference
    if geometry:
        magnet.geometry().associate(Attachment.upload(geometry))
    magnet.save()
    AuditLog.log(user, "Magnet updated", resource=magnet)
    return magnet.serialize()


@router.post("/api/magnets/{id}/defunct")
def defunct(id: int, user=Depends(get_user('update'))):
    magnet = Magnet.with_('magnet_parts.part').find(id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")

    for magnet_part in magnet.magnet_parts:
        magnet_part.part.status = 'in_stock'
        magnet_part.part.save()
        magnet_part.decommissioned_at = datetime.now()
        magnet_part.save()

    magnet.status = 'defunct'
    magnet.save()
    AuditLog.log(user, "Magnet defunct", resource=magnet)
    return magnet.serialize()


@router.delete("/api/magnets/{id}")
def destroy(id: int, user=Depends(get_user('delete'))):
    magnet = Magnet.find(id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")
    magnet.delete()
    AuditLog.log(user, "Magnet deleted", resource=magnet)
    return magnet.serialize()

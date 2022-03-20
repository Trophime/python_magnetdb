from fastapi import APIRouter, Query, HTTPException, UploadFile, Depends
from fastapi.params import File, Form

from ...dependencies import get_user
from ...models.attachment import Attachment
from ...models.audit_log import AuditLog
from ...models.material import Material
from ...models.part import Part

router = APIRouter()


@router.get("/api/parts")
def index(user=Depends(get_user('read')), page: int = 1, per_page: int = Query(default=25, lte=100),
          query: str = Query(None), sort_by: str = Query(None), sort_desc: bool = Query(False)):
    parts = Part
    if query is not None and query.strip() != '':
        parts = parts.where('name', 'ilike', f'%{query}%')
    if sort_by is not None:
        parts = parts.order_by(sort_by, 'desc' if sort_desc else 'asc')
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
    part.save()
    AuditLog.log(user, "Part created", resource=part)
    return part.serialize()


@router.get("/api/parts/{id}")
def show(id: int, user=Depends(get_user('read'))):
    part = Part.with_('material', 'cao', 'geometry', 'magnet_parts.magnet').find(id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    return part.serialize()


@router.patch("/api/parts/{id}")
def update(id: int, user=Depends(get_user('update')), name: str = Form(...), description: str = Form(None),
           type: str = Form(...), material_id: str = Form(...), design_office_reference: str = Form(None),
           cao: UploadFile = File(None), geometry: UploadFile = File(None)):
    part = Part.with_('material', 'cao', 'geometry').find(id)
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
    if cao:
        part.cao().associate(Attachment.upload(cao))
    if geometry:
        part.geometry().associate(Attachment.upload(geometry))
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

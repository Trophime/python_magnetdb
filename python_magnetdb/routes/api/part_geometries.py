from fastapi import APIRouter, HTTPException, Depends, UploadFile
from fastapi.params import Form, File
from python_magnetdb.models.part import Part

from ...dependencies import get_user
from ...models.attachment import Attachment
from ...models.audit_log import AuditLog
from ...models.part_geometry import PartGeometry

router = APIRouter()


@router.post("/api/parts/{part_id}/geometries")
def create(part_id: int, type: str = Form(...), attachment: UploadFile = File(...), user=Depends(get_user('create'))):
    part = Part.find(part_id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    if not type in part.allow_geometry_types():
        raise HTTPException(status_code=422, detail=f"Unsupported type for {part.type}")

    geometry = PartGeometry.where('part_id', part_id).where('type', type).first()
    if not geometry:
        geometry = PartGeometry(part_id=part_id, type=type)
    geometry.attachment().associate(Attachment.upload(attachment))
    geometry.save()
    AuditLog.log(user, "Geometry saved", resource=geometry)
    return geometry.serialize()


@router.delete("/api/parts/{part_id}/geometries/{type}")
def destroy(part_id: int, type: str, user=Depends(get_user('delete'))):
    geometry = PartGeometry.where('part_id', part_id).where('type', type).first()
    if not geometry:
        raise HTTPException(status_code=404, detail="Geometry not found")
    geometry.delete()
    AuditLog.log(user, "Geometry deleted", resource=geometry)
    return geometry.serialize()

from fastapi import APIRouter, HTTPException, Form, Depends
from datetime import datetime

from ...dependencies import get_user
from ...models.audit_log import AuditLog
from ...models.magnet import MagnetPart, Magnet
from ...models.part import Part
from ...models.status import Status

router = APIRouter()


@router.post("/api/magnets/{magnet_id}/parts")
def create(magnet_id: int, user=Depends(get_user("create")), part_id: int = Form(...)):
    magnet = Magnet.find(magnet_id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")
    part = Part.with_("magnet_parts.magnet").find(part_id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    for magnet_part in part.magnet_parts:
        if magnet_part.magnet.status == Status.IN_STUDY:
            magnet_part.delete()

    magnet_part = MagnetPart(commissioned_at=datetime.now())
    magnet_part.magnet().associate(magnet)
    magnet_part.part().associate(part)
    magnet_part.save()

    AuditLog.log(user, "Part added to magnet", resource=magnet)
    return magnet_part.serialize()


"""
# TODO add an update method to change 'commissioned_at', 'decommissioned_at' from models: models/magnet_part.py MagnetPart
# how to get MagnetPart id
@router.patch("/api/magnets/{magnet_id}/parts")
def update(
    id: int,
    user=Depends(get_user("update")),
    part_id: int = Form(...),
    commissioned_at: datetime = datetime.now(),
    decommissioned_at: datetime = datetime.now(),
):
    magnet_part = MagnetPart.with_("cad.attachment", "geometry").find(id)
    if not magnet_part:
        raise HTTPException(status_code=404, detail="MagnetPart not found")

    magnet_part.commissioned_at = commissioned_at
    magnet_part.decommissioned_at = decommissioned_at
    magnet_part.save()
    AuditLog.log(user, "MagnetPart updated", resource=magnet_part)
    return magnet_part.serialize()
"""

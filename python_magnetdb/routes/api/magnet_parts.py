from fastapi import APIRouter, HTTPException, Form, Depends
from datetime import datetime

from ...dependencies import get_user
from ...models.audit_log import AuditLog
from ...models.magnet import MagnetPart, Magnet
from ...models.part import Part

router = APIRouter()


@router.post("/api/magnets/{magnet_id}/parts")
def create(magnet_id: int, user=Depends(get_user('create')), part_id: int = Form(...)):
    magnet = Magnet.find(magnet_id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")
    part = Part.with_('magnet_parts.magnet').find(part_id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    for magnet_part in part.magnet_parts:
        if magnet_part.magnet.status == 'in_study':
            magnet_part.delete()

    magnet_part = MagnetPart(commissioned_at=datetime.now())
    magnet_part.magnet().associate(magnet)
    magnet_part.part().associate(part)
    magnet_part.save()

    AuditLog.log(user, "Part added to magnet", resource=magnet)
    return magnet_part.serialize()

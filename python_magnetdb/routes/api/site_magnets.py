from datetime import datetime

from fastapi import APIRouter, HTTPException, Form, Depends

from ...dependencies import get_user
from ...models.audit_log import AuditLog
from ...models.magnet import Magnet
from ...models.site import Site
from ...models.site_magnet import SiteMagnet

router = APIRouter()


@router.post("/api/sites/{site_id}/magnets")
def create(site_id: int, user=Depends(get_user('create')), magnet_id: int = Form(...)):
    site = Site.find(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    magnet = Magnet.with_('site_magnets.site').find(magnet_id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")

    for site_magnet in magnet.site_magnets:
        if site_magnet.site.status == 'in_study':
            site_magnet.delete()

    site_magnet = SiteMagnet(commissioned_at=datetime.now())
    site_magnet.site().associate(site)
    site_magnet.magnet().associate(magnet)
    site_magnet.save()
    AuditLog.log(user, "Magnet added to site", resource=magnet)
    return site_magnet.serialize()

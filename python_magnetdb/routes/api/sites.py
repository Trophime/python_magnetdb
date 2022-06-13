from datetime import datetime

import orator
from fastapi import Depends, APIRouter, HTTPException, Query, UploadFile, File, Form

from ...dependencies import get_user
from ...models.attachment import Attachment
from ...models.audit_log import AuditLog
from ...models.site import Site

router = APIRouter()


@router.get("/api/sites")
def index(user=Depends(get_user('read')), page: int = 1, per_page: int = Query(default=25, lte=100),
          query: str = Query(None), sort_by: str = Query(None), sort_desc: bool = Query(False)):
    sites = Site
    if query is not None and query.strip() != '':
        sites = sites.where('name', 'ilike', f'%{query}%')
    if sort_by is not None:
        sites = sites.order_by(sort_by, 'desc' if sort_desc else 'asc')
    sites = sites.paginate(per_page, page)
    return {
        "current_page": sites.current_page,
        "last_page": sites.last_page,
        "total": sites.total,
        "items": sites.serialize(),
    }


@router.post("/api/sites")
def create(user=Depends(get_user('create')), name: str = Form(...), description: str = Form(None),
           config: UploadFile = File(None)):
    site = Site(name=name, description=description, status='in_study')
    if config is not None:
        site.config().associate(Attachment.upload(config))
    try:
        site.save()
    except orator.exceptions.query.QueryException as e:
        raise HTTPException(status_code=422, detail="Name already taken.") if e.message.find('sites_name_unique') != -1 else e
    AuditLog.log(user, "Site created", resource=site)
    return site.serialize()


@router.get("/api/sites/{id}")
def show(id: int, user=Depends(get_user('read'))):
    site = Site.with_('config', 'site_magnets.magnet').find(id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site.serialize()


@router.patch("/api/sites/{id}")
def update(id: int, user=Depends(get_user('update')), name: str = Form(...), description: str = Form(None),
           config: UploadFile = File(None)):
    site = Site.find(id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    site.name = name
    site.description = description
    if config:
        site.config().associate(Attachment.upload(config))
    site.save()
    AuditLog.log(user, "Site updated", resource=site)
    return site.serialize()


@router.post("/api/sites/{id}/put_in_operation")
def put_in_operation(id: int, user=Depends(get_user('update'))):
    site = Site.with_('site_magnets.magnet.magnet_parts.part').find(id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    for site_magnet in site.site_magnets:
        site_magnet.magnet.status = 'in_operation'
        site_magnet.magnet.save()
        for magnet_part in site_magnet.magnet.magnet_parts:
            magnet_part.part.status = 'in_operation'
            magnet_part.part.save()

    site.status = 'in_operation'
    site.save()
    AuditLog.log(user, "Site put in operation", resource=site)
    return site.serialize()


@router.post("/api/sites/{id}/shutdown")
def shutdown(id: int, user=Depends(get_user('update'))):
    site = Site.with_('site_magnets.magnet').find(id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    for site_magnet in site.site_magnets:
        site_magnet.magnet.status = 'in_stock'
        site_magnet.magnet.save()
        site_magnet.decommissioned_at = datetime.now()
        site_magnet.save()

    site.status = 'defunct'
    site.save()
    AuditLog.log(user, "Site shutdown", resource=site)
    return site.serialize()


@router.delete("/api/sites/{id}")
def destroy(id: int, user=Depends(get_user('delete'))):
    site = Site.find(id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    site.delete()
    AuditLog.log(user, "Site deleted", resource=site)
    return site.serialize()

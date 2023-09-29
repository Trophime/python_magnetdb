from datetime import datetime
from typing import List

import orator.exceptions.query
from fastapi import APIRouter, Query, HTTPException, Form, UploadFile, File, Depends

from ...dependencies import get_user
from ...models.attachment import Attachment
from ...models.audit_log import AuditLog
from ...models.magnet import Magnet
from ...models.status import Status

from ...actions.generate_magnet_directory import generate_magnet_directory

router = APIRouter()


@router.get("/api/magnets")
def index(user=Depends(get_user('read')), page: int = 1, per_page: int = Query(default=25, lte=100),
          query: str = Query(None), sort_by: str = Query(None), sort_desc: bool = Query(False),
          status: List[str] = Query(default=None, alias="status[]")):
    magnets = Magnet.with_('site_magnets') \
        .order_by(sort_by or 'created_at', 'desc' if sort_desc else 'asc')
    if query is not None and query.strip() != '':
        magnets = magnets.where('name', 'ilike', f'%{query}%')
    if status is not None:
        magnets = magnets.where_in('status', status)
    magnets = magnets.paginate(per_page, page)

    items = []
    for magnet in magnets:
        item = magnet.serialize()
        item["commissioned_at"] = (
            sorted(
                list(map(lambda curr: curr.commissioned_at, magnet.site_magnets)),
                reverse=True,
            )[0]
            if len(magnet.site_magnets) > 0
            else None
        )
        decommissioned_at = list(
            filter(
                lambda curr: curr is not None,
                map(lambda curr: curr.decommissioned_at, list(magnet.site_magnets)),
            )
        )
        item["decommissioned_at"] = (
            sorted(decommissioned_at, reverse=True)[0]
            if len(decommissioned_at) > 0
            else None
        )
        items.append(item)

    return {
        "current_page": magnets.current_page,
        "last_page": magnets.last_page,
        "total": magnets.total,
        "items": items,
    }


@router.post("/api/magnets")
def create(
    user=Depends(get_user("create")),
    name: str = Form(...),
    description: str = Form(None),
    design_office_reference: str = Form(None),
):
    magnet = Magnet(
        name=name,
        description=description,
        design_office_reference=design_office_reference,
        status=Status.IN_STUDY,
    )
    try:
        magnet.save()
    except orator.exceptions.query.QueryException as e:
        if e.message.find("magnets_name_unique") != -1:
            raise HTTPException(status_code=422, detail="Name already taken.")
        raise e

    AuditLog.log(user, "Magnet created", resource=magnet)
    return magnet.serialize()


@router.get("/api/magnets/{id}/sites")
def sites(id: int, user=Depends(get_user("read"))):
    magnet = Magnet.with_("site_magnets.site").find(id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")

    result = []
    for site_magnet in magnet.site_magnets:
        result.append(site_magnet.serialize())
    return {"sites": result}


@router.get("/api/magnets/{id}/records")
def records(id: int, user=Depends(get_user("read"))):
    magnet = Magnet.with_("site_magnets.site.records").find(id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")

    result = []
    for site_magnet in magnet.site_magnets:
        for record in site_magnet.site.records:
            result.append(record.serialize())
    return {"records": result}


@router.get("/api/magnets/{id}/mdata")
def mdata(id: int, user=Depends(get_user("read"))):
    magnet = Magnet.find(id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")

    data = generate_magnet_directory(id)
    return {"results": data}


@router.get("/api/magnets/{id}")
def show(id: int, user=Depends(get_user("read"))):
    magnet = Magnet.with_(
        "magnet_parts.part", "site_magnets.site", "cad.attachment", "geometry"
    ).find(id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")

    res = magnet.serialize()
    res["commissioned_at"] = (
        sorted(
            list(map(lambda curr: curr.commissioned_at, list(magnet.site_magnets))),
            reverse=True,
        )[0]
        if len(magnet.site_magnets) > 0
        else None
    )
    decommissioned_at = list(
        filter(
            lambda curr: curr is not None,
            map(lambda curr: curr.decommissioned_at, list(magnet.site_magnets)),
        )
    )
    res["decommissioned_at"] = (
        sorted(decommissioned_at, reverse=True)[0]
        if len(decommissioned_at) > 0
        else None
    )
    return res


@router.patch("/api/magnets/{id}")
def update(
    id: int,
    user=Depends(get_user("update")),
    name: str = Form(...),
    description: str = Form(None),
    design_office_reference: str = Form(None),
    geometry: UploadFile = File(None),
):
    magnet = Magnet.with_("cad.attachment", "geometry").find(id)
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
def defunct(id: int, decommissioned_at: datetime = Form(datetime.now()), user=Depends(get_user('update'))):
    magnet = Magnet.with_('magnet_parts.part').find(id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")

    for magnet_part in magnet.magnet_parts:
        if not magnet_part.active:
            continue
        magnet_part.part.status = Status.IN_STOCK
        magnet_part.part.save()
        magnet_part.decommissioned_at = decommissioned_at
        magnet_part.save()

    magnet.status = Status.DEFUNCT
    magnet.save()
    AuditLog.log(user, "Magnet defunct", resource=magnet)
    return magnet.serialize()


@router.delete("/api/magnets/{id}")
def destroy(id: int, user=Depends(get_user("delete"))):
    magnet = Magnet.find(id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")
    magnet.delete()
    AuditLog.log(user, "Magnet deleted", resource=magnet)
    return magnet.serialize()

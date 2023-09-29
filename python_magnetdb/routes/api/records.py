from typing import Optional

from datetime import datetime

import pandas as pd
from pydantic import BaseModel
from fastapi import APIRouter, Query, HTTPException, Form, UploadFile, File, Depends

from ...dependencies import get_user
from ...models.attachment import Attachment
from ...models.audit_log import AuditLog
from ...models.record import Record
from ...models.site import Site
from ...utils.record_visualization import columns as columns_with_name

router = APIRouter()


@router.get("/api/records")
def index(user=Depends(get_user('read')), page: int = 1, per_page: int = Query(default=25, lte=100),
          query: str = Query(None), sort_by: str = Query(None), sort_desc: bool = Query(False)):
    records = Record \
        .order_by(sort_by or 'created_at', 'desc' if sort_desc else 'asc')
    if query is not None and query.strip() != '':
        records = records.where('name', 'ilike', f'%{query}%')
    records = records.paginate(per_page, page)
    return {
        "current_page": records.current_page,
        "last_page": records.last_page,
        "total": records.total,
        "items": records.serialize(),
    }


@router.post("/api/records")
def create(user=Depends(get_user('create')), name: str = Form(...), description: str = Form(None),
           site_id: str = Form(...), attachment: UploadFile = File(...)):
    site = Site.find(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    record = Record(name=name, description=description)
    record.attachment().associate(Attachment.upload(attachment))
    record.site().associate(site)
    record.save()
    AuditLog.log(user, f"Record created {attachment.filename}", resource=record)
    return record.serialize()

class RecordPayload(BaseModel):
    name: str
    description: Optional[str]
    site_id: int
    attachment_id: int
    
@router.post("/api/clirecords")
def clicreate(payload: RecordPayload, user=Depends(get_user('create'))):
    print(f'record/clicreate: name={payload.name}, attachment_id={payload.attachment_id}')
    site = Site.find(payload.site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    print(f'site: {site}')

    attachment = Attachment.find(payload.attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    print(f'attachment: {attachment}')

    record = Record(name=payload.name, description=payload.description)
    record.attachment().associate(attachment)
    print(f'record/clicreate: associate attachment done')
    record.site().associate(site)
    print(f'record/clicreate: associate site done')
    record.save()
    AuditLog.log(user, f"Record cli created {payload.name}", resource=record)
    return record.serialize()

@router.get("/api/records/{id}")
def show(id: int, user=Depends(get_user('read'))):
    record = Record.with_('attachment', 'site').find(id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    return record.serialize()


@router.get("/api/records/{id}/visualize")
def visualize(id: int, user=Depends(get_user('read')),
              x: str = Query(None), y: str = Query(None), auto_sampling: bool = Query(False),
              x_min: float = Query(None), x_max: float = Query(None),
              y_min: float = Query(None), y_max: float = Query(None)):
    record = Record.with_('attachment').find(id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    # data prep
    time_format = "%Y.%m.%d %H:%M:%S"
    data = pd.read_csv(record.attachment.download(), sep=r'\s+', skiprows=1)
    # cleanup: remove empty columns
    data = data.loc[:, (data != 0.0).any(axis=0)]
    t0 = datetime.strptime(data['Date'].iloc[0] + " " + data['Time'].iloc[0], time_format)
    data["t"] = data.apply(
        lambda row: (datetime.strptime(row.Date + " " + row.Time, time_format) - t0).total_seconds(),
        axis=1
    )
    data["timestamp"] = data.apply(lambda row: datetime.strptime(row.Date + " " + row.Time, time_format), axis=1)

    result = {}
    sampling_enabled = False
    if x is not None and y is not None:
        y = y.split(',')

        # to handle chart resizing
        if x_min is not None and x_max is not None and y_min is not None and y_max is not None:
            data = data[(data[x] >= x_min) & (data[x] <= x_max)]
            for y_value in y:
                data = data[(data[y_value] >= y_min) & (data[y_value] <= y_max)]

        # compute if sampling is required
        sampling_enabled = auto_sampling is True and len(data) > 500
        sampling_factor = round(data['timestamp'].count() / 500) if sampling_enabled else 1

        # rendering values and applying sampling factor is needed
        for (index, values) in enumerate(data[[x] + y].values):
            if index % sampling_factor == 0:
                result[values[0]] = values[1:].tolist()

    columns = {}
    for column in data.columns.tolist():
        columns[column] = columns_with_name[column]

    return {'result': result, 'columns': columns, 'sampling_enabled': sampling_enabled}


@router.patch("/api/records/{id}")
def update(id: int, user=Depends(get_user('update')), name: str = Form(...), description: str = Form(None),
           site_id: str = Form(...)):
    record = Record.find(id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    site = Site.find(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    record.name = name
    record.description = description
    record.site().associate(site)
    record.save()
    AuditLog.log(user, "Record updated", resource=record)
    return record.serialize()


@router.delete("/api/records/{id}")
def destroy(id: int, user=Depends(get_user('delete'))):
    record = Record.find(id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    record.delete()
    AuditLog.log(user, "Record deleted", resource=record)
    return record.serialize()

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.responses import StreamingResponse

from ...dependencies import get_user
from ...models.audit_log import AuditLog
from ...models.attachment import Attachment

router = APIRouter()


@router.get("/api/attachments/{id}/download")
def download(id: int, user=Depends(get_user('read'))):
    attachment = Attachment.find(id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    return StreamingResponse(attachment.download(), media_type=attachment.content_type, headers={
        'content-disposition': f'attachment; filename="{attachment.filename}"'
    })

class FilePayload(BaseModel):
    filename: str
    content_type: str
    fileno: int

@router.post("/api/attachments")
def upload(file: UploadFile = File(...), user=Depends(get_user('create'))):
    attached = Attachment.upload(file)
    try:
        attached.save()
    except orator.exceptions.query.QueryException as e:
        raise HTTPException(status_code=422, detail=e.message)
    AuditLog.log(user, f"Attachment created {file.filename}", resource=attached)
    return attached.serialize()

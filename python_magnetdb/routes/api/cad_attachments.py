from fastapi import APIRouter, UploadFile, Depends, File, HTTPException, Form

from python_magnetdb.dependencies import get_user
from python_magnetdb.models.attachment import Attachment
from python_magnetdb.models.cad_attachment import CadAttachment
from python_magnetdb.models.magnet import Magnet
from python_magnetdb.models.part import Part

router = APIRouter()


@router.post("/api/cad_attachments")
def create(resource_id: str = Form(...), resource_type: str = Form(...),
            file: UploadFile = File(...), user=Depends(get_user('update'))):
    if resource_type == 'magnet':
        resource = Magnet.find(resource_id)
    elif resource_type == 'part':
        resource = Part.find(resource_id)

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    cad_attachment = CadAttachment()
    cad_attachment.resource().associate(resource)
    cad_attachment.attachment().associate(Attachment.upload(file))
    cad_attachment.save()
    return cad_attachment.serialize()


@router.delete("/api/cad_attachments/{id}")
def destroy(id: int, user=Depends(get_user('update'))):
    cad_attachment = CadAttachment.find(id)
    if not cad_attachment:
        raise HTTPException(status_code=404, detail="CAD Attachment not found")

    cad_attachment.delete()
    return cad_attachment.serialize()

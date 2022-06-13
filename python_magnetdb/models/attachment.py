from uuid import uuid4

from fastapi import UploadFile
from orator import Model

from ..storage import s3_client, s3_bucket


class Attachment(Model):
    __table__ = "storage_attachments"
    __fillable__ = ['key', 'filename', 'content_type']

    def download(self, path=None):
        if path is not None:
            return s3_client.fget_object(s3_bucket, self.key, path)

        return s3_client.get_object(s3_bucket, self.key)

    @classmethod
    def upload(cls, file: UploadFile):
        return cls.raw_upload(filename=file.filename, content_type=file.content_type, fileno=file.file.fileno())

    @classmethod
    def raw_upload(cls, filename: str, content_type: str, fileno: int):
        attachment = cls.create({
            "key": str(uuid4()),
            "filename": filename,
            "content_type": content_type,
        })
        s3_client.fput_object(s3_bucket, attachment.key, fileno, content_type=attachment.content_type)
        return attachment


class AttachmentObserver(object):
    def deleting(self, attachment):
        s3_client.remove_object(s3_bucket, attachment.key)


Attachment.observe(AttachmentObserver())

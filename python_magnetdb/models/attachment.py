from uuid import uuid4

from fastapi import UploadFile
from orator import Model

from ..storage import s3_client, s3_bucket


class Attachment(Model):
    __table__ = "storage_attachments"
    __fillable__ = ['key', 'filename', 'content_type']

    def download(self):
        return s3_client.get_object(s3_bucket, self.key)

    @classmethod
    def upload(cls, file: UploadFile):
        attachment = cls.create({
            "key": str(uuid4()),
            "filename": file.filename,
            "content_type": file.content_type,
        })
        s3_client.fput_object(s3_bucket, attachment.key, file.file.fileno(), content_type=attachment.content_type)
        return attachment

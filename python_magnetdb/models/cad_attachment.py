from orator import Model
from orator.orm import belongs_to, morph_to


class CadAttachment(Model):
    __table__ = "cad_attachments"
    __fillable__ = ['attachment_id', 'resource_id', 'resource_type']

    @morph_to
    def resource(self):
        return

    @belongs_to('attachment_id')
    def attachment(self):
        from python_magnetdb.models.attachment import Attachment
        return Attachment

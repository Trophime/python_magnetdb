from orator import Model
from orator.orm import belongs_to


class Record(Model):
    __table__ = "records"
    __fillable__ = ['name', 'description', 'site_id', 'attachment_id']

    @belongs_to('site_id')
    def site(self):
        from .site import Site
        return Site

    @belongs_to('attachment_id')
    def attachment(self):
        from .attachment import Attachment
        return Attachment

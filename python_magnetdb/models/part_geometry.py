from orator import Model
from orator.orm import belongs_to


class PartGeometry(Model):
    __table__ = "part_geometries"
    __fillable__ = ['part_id', 'type', 'attachment_id']

    @belongs_to('part_id')
    def part(self):
        from .part import Part
        return Part

    @belongs_to('attachment_id')
    def attachment(self):
        from .attachment import Attachment
        return Attachment

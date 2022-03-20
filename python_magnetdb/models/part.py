from orator import Model
from orator.orm import belongs_to, has_many, has_many_through

from .attachment import Attachment
from .magnet_part import MagnetPart
from .material import Material


class Part(Model):
    __table__ = "parts"
    __fillable__ = ['name', 'description', 'status', 'type', 'design_office_reference', 'material_id']

    @belongs_to('geometry_attachment_id')
    def geometry(self):
        return Attachment

    @belongs_to('cao_attachment_id')
    def cao(self):
        return Attachment

    @belongs_to('material_id')
    def material(self):
        return Material

    @has_many
    def magnet_parts(self):
        return MagnetPart

    @has_many_through(MagnetPart, 'part_id', 'id')
    def magnets(self):
        from .magnet import Magnet
        return Magnet

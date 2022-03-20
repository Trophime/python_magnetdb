from orator import Model
from orator.orm import belongs_to


class MagnetPart(Model):
    __table__ = "magnet_parts"
    __fillable__ = ['commissioned_at', 'decommissioned_at']

    @belongs_to('magnet_id')
    def magnet(self):
        from .magnet import Magnet
        return Magnet

    @belongs_to('part_id')
    def part(self):
        from .part import Part
        return Part

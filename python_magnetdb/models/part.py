from orator import Model
from orator.orm import belongs_to, has_many, has_many_through, morph_many

from .magnet_part import MagnetPart


class Part(Model):
    __table__ = "parts"
    __fillable__ = ['name', 'description', 'status', 'type', 'design_office_reference', 'material_id']

    def allow_geometry_types(self):
        if self.type == 'helix':
            return ['default', 'salome', 'catia', 'cam', 'shape']
        elif self.type == 'supra':
            return ['default', 'hts']
        return ['default']

    @has_many
    def geometries(self):
        from python_magnetdb.models.part_geometry import PartGeometry
        return PartGeometry

    @morph_many('resource')
    def cad(self):
        from python_magnetdb.models.cad_attachment import CadAttachment
        return CadAttachment

    @belongs_to('material_id')
    def material(self):
        from python_magnetdb.models.material import Material
        return Material

    @has_many
    def magnet_parts(self):
        return MagnetPart

    @has_many_through(MagnetPart, 'part_id', 'id')
    def magnets(self):
        from .magnet import Magnet
        return Magnet

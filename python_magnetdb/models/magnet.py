from orator import Model
from orator.orm import belongs_to, has_many, has_many_through, morph_many

from .attachment import Attachment
from .cad_attachment import CadAttachment
from .magnet_part import MagnetPart
from .site_magnet import SiteMagnet


class Magnet(Model):
    __table__ = "magnets"
    __fillable__ = ['name', 'description', 'status', 'design_office_reference']

    @belongs_to('geometry_attachment_id')
    def geometry(self):
        return Attachment

    @morph_many('resource')
    def cad(self):
        return CadAttachment

    @has_many
    def magnet_parts(self):
        return MagnetPart

    @has_many_through(MagnetPart, 'magnet_id', 'id')
    def parts(self):
        from .part import Part
        return Part

    @has_many
    def site_magnets(self):
        return SiteMagnet

    @has_many_through(SiteMagnet)
    def sites(self):
        from .site import Site
        return Site

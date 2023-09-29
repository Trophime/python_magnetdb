from orator import Model
from orator.orm import belongs_to, has_many, has_many_through

from .attachment import Attachment
from .site_magnet import SiteMagnet


class Site(Model):
    __table__ = "sites"
    __fillable__ = ['name', 'description', 'status']

    @belongs_to('config_attachment_id')
    def config(self):
        return Attachment

    @has_many
    def records(self):
        from .record import Record
        return Record

    @has_many
    def site_magnets(self):
        return SiteMagnet

    @has_many_through(SiteMagnet, 'site_id', 'id')
    def magnets(self):
        from .magnet import Magnet
        return Magnet

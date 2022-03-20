from orator import Model
from orator.orm import belongs_to


class SiteMagnet(Model):
    __table__ = "site_magnets"
    __fillable__ = ['commissioned_at', 'decommissioned_at']

    @belongs_to('magnet_id')
    def magnet(self):
        from .magnet import Magnet
        return Magnet

    @belongs_to('site_id')
    def site(self):
        from .site import Site
        return Site

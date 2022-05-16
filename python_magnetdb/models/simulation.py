from orator import Model
from orator.orm import belongs_to, morph_to


class Simulation(Model):
    __table__ = "simulations"
    __fillable__ = ['resource_id', 'resource_type', 'method', 'model', 'geometry', 'cooling', 'static', 'non_linear',
                    'setup_status', 'setup_attachment_id', 'status', 'output_attachment_id']

    @morph_to
    def resource(self):
        return

    @belongs_to('setup_output_attachment_id')
    def setup_output_attachment(self):
        from .attachment import Attachment
        return Attachment

    @belongs_to('output_attachment_id')
    def output_attachment(self):
        from .attachment import Attachment
        return Attachment

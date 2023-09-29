from orator import Model
from orator.orm import belongs_to, morph_to, has_many


class Simulation(Model):
    __table__ = "simulations"
    __fillable__ = ['resource_id', 'resource_type', 'method', 'model', 'geometry', 'cooling', 'static', 'non_linear',
                    'setup_status', 'setup_attachment_id', 'status', 'output_attachment_id', 'setup_state', 'owner_id',
                    'log_attachment_id']
    __casts__ = {
        'setup_state': 'dict'
    }

    @morph_to
    def resource(self):
        return

    @has_many
    def currents(self):
        from .simulation_current import SimulationCurrent
        return SimulationCurrent

    @belongs_to('setup_output_attachment_id')
    def setup_output_attachment(self):
        from .attachment import Attachment
        return Attachment

    @belongs_to('output_attachment_id')
    def output_attachment(self):
        from .attachment import Attachment
        return Attachment

    @belongs_to('log_attachment_id')
    def log_attachment(self):
        from .attachment import Attachment
        return Attachment

    @belongs_to('owner_id')
    def owner(self):
        from .user import User
        return User


class SimulationObserver(object):
    def deleting(self, simulation):
        from .attachment import Attachment

        if simulation.setup_output_attachment_id is not None:
            setup_output_attachment = Attachment.find(simulation.setup_output_attachment_id)
            if setup_output_attachment is not None:
                setup_output_attachment.delete()
        if simulation.output_attachment_id is not None:
            output_attachment = Attachment.find(simulation.output_attachment_id)
            if output_attachment is not None:
                output_attachment.delete()
        if simulation.log_attachment_id is not None:
            log_attachment = Attachment.find(simulation.log_attachment_id)
            if log_attachment is not None:
                log_attachment.delete()


Simulation.observe(SimulationObserver())

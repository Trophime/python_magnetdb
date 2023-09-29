from orator import Model
from orator.orm import belongs_to


class SimulationCurrent(Model):
    __table__ = "simulation_currents"
    __fillable__ = ['simulation_id', 'magnet_id', 'value']

    @belongs_to('simulation_id')
    def simulation(self):
        from .simulation import Simulation
        return Simulation

    @belongs_to('magnet_id')
    def magnet(self):
        from .magnet import Magnet
        return Magnet

from orator import Model
from orator.orm import has_many


class Material(Model):
    __table__ = "materials"
    __fillable__ = ['name', 'nuance', 'description', 't_ref', 'volumic_mass', 'alpha', 'specific_heat',
                    'electrical_conductivity', 'thermal_conductivity', 'magnet_permeability', 'young',
                    'poisson', 'expansion_coefficient', 'rpe']

    @has_many
    def parts(self):
        from .part import Part
        return Part

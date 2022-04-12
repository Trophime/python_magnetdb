from pint import UnitRegistry

ureg = UnitRegistry(system='SI')
volumicmass = 1* ureg.kilogram / ureg.meter**3
ThermalConductivity = 1 * ureg.watt / ureg.meter / ureg.kelvin
tref = 1 * ureg.kelvin
specificheat = 1 * ureg.joule / ureg.kelvin / ureg.kilogram
alpha = 1 / ureg.kelvin
electricalconductivity = 1 * ureg.siemens / ureg.meter
thermalconductivity = 1 * ureg.watt / ureg.meter / ureg.kelvin
young = 1 * ureg.pascal
coefdilatation = 1 / ureg.kelvin
rpe = 1 * ureg.pascal

# stored units
        
units = {
    'Tref': '[{:~P}]'.format(tref.units),
    'VolumicMass': '[{:~P}]'.format(volumicmass.units),
    'SpecificHeat': '[{:~P}]'.format(specificheat.units),
    'alpha': '[{:~P}]'.format(alpha.units),
    'ElectricalConductivity': '[{:~P}]'.format(electricalconductivity.units),
    'ThermalConductivity': '[{:~P}]'.format(thermalconductivity.units),
    'MagnetPermeability': "[SI]",
    'Young': '[{:~P}]'.format(young.units),
    'Poisson': "[SI]",
    'CoefDilatation': '[{:~P}]'.format(coefdilatation.units),
    'Rpe': '[{:~P}]'.format(rpe.units),
    'Nuance': "",
    'Furnisher': "",
    'Ref': ""
}

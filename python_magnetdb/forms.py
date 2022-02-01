"""Form object declaration."""
from typing import List, Optional

# from flask_wtf import FlaskForm
from starlette_wtf import StarletteForm
from wtforms import StringField, FloatField, SelectField, BooleanField, SubmitField, FieldList, FormField, ValidationError
from wtforms.validators import DataRequired, Length


from .units import units
from .status import MStatus, status_choices
from .status import MType, mtype_choices

from .choices import material_choices
from .choices import objchoices

def coerce_for_enum(enum):
    def coerce(name):
        print("coerce_for_enum:", name, type(name))
        if isinstance(name, enum):
            return name
        try:
            return enum[name]
        except KeyError:
            print("fuckup", name, type(name))
            raise ValueError(name)
    return coerce


class MaterialForm(StarletteForm):
    """
    Material Physical Properties in SI for isotropic material
    """

    name =  StringField('Name', validators=[DataRequired()])
    Tref = FloatField('Tref ' + units['Tref'], validators=[DataRequired()])

    VolumicMass = FloatField('VolumicMass ' + units['VolumicMass'], validators=[DataRequired()])
    SpecificHeat = FloatField('SpecificHeat ' + units['SpecificHeat'], validators=[DataRequired()])

    alpha = FloatField('alpha ' + units['alpha'], validators=[DataRequired()])
    ElectricalConductivity = FloatField('ElectricalConductivity ' + units['ElectricalConductivity'], validators=[DataRequired()])
    ThermalConductivity = FloatField('ThermalConductivity ' + units['ThermalConductivity'], validators=[DataRequired()])
    MagnetPermeability = FloatField('MagnetPermeability', validators=[DataRequired()])

    Young = FloatField('Young ' + units['Young'], validators=[DataRequired()])
    Poisson = FloatField('Poisson', validators=[DataRequired()])
    CoefDilatation = FloatField('CoefDilatation ' + units['CoefDilatation'], validators=[DataRequired()])
    Rpe = FloatField('Rpe ' + units['Rpe'], validators=[DataRequired()])

    nuance = StringField('Nuance', validators=[DataRequired()])
    furnisher = StringField('Furnisher', validators=[DataRequired()])
    ref = StringField('Ref', validators=[DataRequired()])

from .magnetfield import MPartListField, BetterMagnetListField

class MPartForm(StarletteForm):
    """
    MPart 
    """
    name =  StringField('Name', validators=[DataRequired()])

    mtype = StringField('Type', choices=mtype_choices, validators=[DataRequired()])
    be = StringField('Be Ref', validators=[DataRequired()])
    geom = StringField('Geom', validators=[DataRequired()])
    status = SelectField('Status', choices=status_choices, validators=[DataRequired()])

    # TODO create liste of materials choice
    material_id = SelectField('Material', choices=material_choices(), validators=[DataRequired()])
    magnets = BetterMagnetListField('Magnets') # FieldList(FormField(MPartForm)) not working


class MagnetForm(StarletteForm):
    """
    Magnet 
    """
    print("MagnetForm")
    name =  StringField('Name', validators=[DataRequired()])

    be = StringField('Be Ref', validators=[DataRequired()])
    geom = StringField('Geom', validators=[DataRequired()])
    status = SelectField('Status', choices=status_choices)
    mparts = MPartListField('Parts') # FieldList(FormField(MPartForm)) not working
    # msites = FieldList(StringField('Sites'))

class MSiteForm(StarletteForm):
    """
    Magnet Site
    """
    
    name =  StringField('Name', validators=[DataRequired()])
    conffile: StringField('Conffile', validators=[DataRequired()]) # FileField?? or MultipleFileField??
    status = SelectField('Status', choices=status_choices)

class GeomForm(StarletteForm):
    """
    Yaml geom configuration
    """

    name =  StringField('Name', validators=[DataRequired()])

method_choices = [ ('cfpdes','cfpdes'), ('CG','CG'), ('HDG','HDG'), ('CRB','CRB') ]
model_choices = [('thelec','thelec'), ('mag','mag'), ('thmag','thmag'), ('thmagel', 'thmagel')]
geom_choices = [ ('Axi','Axi'), ('3D','3D')]
cooling_choices = [ ('mean','mean'), ('grad','grad'), ('meanH','meanH'), ('gradH','gradH')]

class SimulationForm(StarletteForm):
    """
    Simulation SetUp configuration
    """
    print("SimulationForm")
    method = SelectField('Method', choices=method_choices)
    model = SelectField('Model', choices=model_choices) # shall depend on method choice
    geom = SelectField('Geom', choices=geom_choices)
    cooling = SelectField('Geom', choices=cooling_choices)
    static = BooleanField('Static') # bool
    linear = BooleanField('Linear') # bool

    # mstatus = SelectField('Status', choices=status_choices) # actually a choice "Magnet/Site"

    mobject = SelectField('Name')    

class BmapForm(StarletteForm):
    """
    Bmap SetUp configuration
    """
    print("BmapForm")
    
    mobject = SelectField('Name') # choices=objchoices('Magnet', None))    
    

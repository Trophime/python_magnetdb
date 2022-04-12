import enum

class MStatus(str, enum.Enum):
    study = "in_study"
    operation = "in_operation"
    stock = "in_stock"
    defunct = "defunct"

class MType(str, enum.Enum):
    Helix = "Helix",
    Ring = "Ring",
    Lead = "Lead",
    Bitter = "Bitter",
    Supra = "Supra"
    Screen = "Screen"

status_choices = [(v.value, v.name) for v in MStatus]
mtype_choices = [(v.value, v.name) for v in MType]
    

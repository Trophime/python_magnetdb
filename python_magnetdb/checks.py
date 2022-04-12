from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Session, select

from .models import MPart, Magnet, MSite, MRecord
from .models import MaterialBase, Material, MaterialCreate, MaterialRead
from .models import MPartMagnetLink, MagnetMSiteLink
from .models import MStatus

def check_material(session: Session, id: int):
    """
    Check if properties are defined for Material with id
    """
    material = session.get(Material, id)
    data = material.dict()
    defined =  material.dict(exclude_defaults=True)
    undef_set = set(data.keys()) - set(defined.keys())
    return undef_set
    

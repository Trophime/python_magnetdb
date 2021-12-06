from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Session, select

from .database import engine
from .models import Material

from .models import MPart, Magnet, MSite, MRecord
from .models import MaterialBase, Material, MaterialCreate, MaterialRead
from .models import MPartMagnetLink, MagnetMSiteLink
from .models import MStatus
from .units import units

from .queries import query_mpart, query_magnet, query_msite, query_material
from .crud import get_magnet_type

import yaml


def material_choices():
    with Session(engine) as session:
        statement = select(Material)
        results = session.exec(statement).all()
    
    choices = []
    for obj in results:
        desc = obj.name + " (" + obj.nuance + "," + "Rpe:" + str(obj.Rpe) + units['Rpe'] + ")"
        choices.append( (obj.id, desc))
    
    return choices

def mpart_choices(mtype: str, status: MStatus):
    with Session(engine) as session:
        statement = select(MPart).where(MPart.mtype == mtype).where(MPart.status == status)
        results = session.exec(statement).all()
    
    choices = []
    for obj in results:
        desc = obj.name

        # Get Material
        material = select(Material).where(Material.id == obj.material_id)
        desc += " (" + material.name + ":" + obj.nuance + "," + "Rpe:" + obj.rpe + units['Rpe'] + ")"
        
        # TODO load obj.geom to get basic geom infos
        # geom = yaml.load(open(obj.name, 'r'))

        choices.append( (obj, desc))
    
    return choices

def magnet_choices(status: Optional[MStatus]):
    with Session(engine) as session:
        print("magnet_choices: status=", status)
        if status:
            #print("magnet_choices: status=", status)
            statement = select(Magnet).where(Magnet.status == status)
            # results = session.exec(statement).all()
        else:
            # print("magnet_choices: status=", status)
            statement = select(Magnet)
        results = session.exec(statement).all()
    
        choices = []
        for obj in results:
            desc = obj.name

            # TODO add magnet type (aka Insert, Bitter or Supra)
            (mtype, components) = get_magnet_type(session, obj.id)
            desc += "(" + mtype + ")"

            # TODO load obj.geom to get basic geom infos (aka inner/outer diameter)
            # geom = yaml.load(open(obj.name, 'r'))

            choices.append( (obj, desc))
    
    if status:
        print("magnet_choices(%s):" % (status), [tobj[0].name for tobj in choices ])
    else:
        print("magnet_choices():", [tobj[0].name for tobj in choices ])
        
    return choices

def msite_choices(status: Optional[MStatus]):
    with Session(engine) as session:
        print("msite_choices: status=", status)
        if status:
            statement = select(MSite).where(MSite.status == status)
        else:
            statement = select(MSite)
        results = session.exec(statement).all()
    
        choices = []
        for obj in results:
            desc = obj.name

            # TODO add msite composition (aka Insert + Bitter + Supra)
            desc += "("
            for magnet in obj.magnets:
                (mtype, components) = get_magnet_type(session, magnet.id)
                desc += magnet.name + ":" + mtype + "," + str(len(components)) + " objects, "
            # TODO remove last ','
            last_char_index = desc.rfind(',')
            desc = desc[:last_char_index] + "," + desc[last_char_index+1:]
            desc += ")"
        
            choices.append( (obj, desc))
    
    return choices

def objchoices(mtype: str, mstatus: Optional[MStatus]):
    print("objchoices:", "mtype=", mtype, "mstatus=", mstatus)
    if mtype == "MSite":
        return msite_choices(mstatus)
    elif mtype == "Magnet":
        return magnet_choices(mstatus)
    else:
        print("objchoices: %s unsupported type of object requested" % mtype)



    
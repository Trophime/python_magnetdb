from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Session, select

from .models import MPart, Magnet, MSite, MRecord, Material
from .models import MPartMagnetLink, MagnetMSiteLink
from .models import MStatus

def query_material(session: Session, name: str):
    statement = select(Material).where(Material.name == name)
    results = session.exec(statement)
    return results

def query_mpart(session: Session, name: str):
    statement = select(MPart).where(MPart.name == name)
    results = session.exec(statement)
    return results

def query_magnet(session: Session, name: str):
    statement = select(Magnet).where(Magnet.name == name)
    results = session.exec(statement)
    return results

def query_msite(session: Session, name: str):
    statement = select(MSite).where(MSite.name == name)
    results = session.exec(statement)
    return results

def query_mrecord_date(session: Session, id: int):
    statement = select(MRecord).where(MSite.msite_id == id)
    results = session.exec(statement)
    print("query_mrecord_date: ", type(results))
    return results

def query_mrecord_site(session: Session, id: int):
    statement = select(MRecord).where(MSite.msite_id == id)
    results = session.exec(statement)
    print("query_mrecord_site: ", type(results))
    return results

def query_mrecord_magnet(session: Session, id: int):
    # get site that contains magnet with id == id
    # for each site get record list
    # sort list by ascending date
    statement = select(MSite, MagnetMSiteLink).join(MSite).where(MagnetMSiteLink.magnet_id == id)
    results = session.exec(statement)
    return results

def query_mrecord_part(session: Session, id: int):
    # get magnet that contains part with id == id
    # for each magnet get site that contains magnet
    # for each site get record list
    # sort list by ascending date
    
    results = []

    statement = select(Magnet, MPartMagnetLink).join(Magnet).where(MPartMagnetLink.mpart_id == id)
    m_res = session.exec(statement)
    for magnet in m_res:
        statement = select(MSite, MagnetMSiteLink).join(MSite).where(MagnetMSiteLink.magnet_id == magnet.id)
        res = session.exec(statement)
        results += res

    return results


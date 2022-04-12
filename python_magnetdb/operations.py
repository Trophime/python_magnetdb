from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Session, select

from .models import MPart, Magnet, MSite, MRecord
from .models import MaterialBase, Material, MaterialCreate, MaterialRead
from .models import MPartMagnetLink, MagnetMSiteLink
from .models import MStatus

from .queries import query_mpart, query_magnet, query_msite
from .crud import get_mparts, get_magnets 

def magnet_add_mpart(session: Session, magnet: Magnet, mpart: MPart ):
    mpart.magnets.append(magnet)
    session.commit()
    session.refresh(mpart)
    pass 

def magnet_delete_mpart(session: Session, magnet: Magnet, mpart: MPart ):
    mpart.magnets.remove(magnet)
    session.commit()
    session.refresh(mpart)
    pass 

def magnet_replace_mpart(session: Session, name: str, impart: str, ompart: str ):
    results = query_magnet(session, name)
    for magnet in results:
        print(magnet)
        
        # remove impart from magnet
        res_parts = query_mpart(session, impart)
        for part in res_parts:
            magnet_delete_mpart(session, magnet, part)
        
        # add ompart to magnet
        res_parts = query_mpart(session, ompart)
        for part in res_parts:
            magnet_add_mpart(session, magnet, part)
    pass 

def msite_add_magnet(session: Session, msite: MSite, magnet: Magnet):
    msite.magnets.append(magnet)
    session.commit()
    session.refresh(msite)
    pass 

def msite_delete_magnet(session: Session, msite: MSite, magnet: Magnet):
    msite.magnets.remove(magnet)
    session.commit()
    session.refresh(msite)
    pass 

def msite_replace_magnet(session: Session, name: str, impart: str, ompart: str):
    results = query_msite(session, name)
    for msite in results:
        print(msite)
        
        # remove impart from magnet
        res = query_magnet(session, impart)
        for part in res:
            msite_delete_magnet(session, msite, res)
        
        # add ompart to magnet
        res = query_magnet(session, ompart)
        for part in res:
            msite_add_magnet(session, msite, res)
    pass 

def duplicate_magnet(session: Session, iname: str, oname: str ):
    msites : List[MSite] = []
    results = query_magnet(session, iname)
    for imagnet in results:
        print(imagnet)
        mparts = get_mparts(session, imagnet.id)

        magnet = Magnet(name=oname, be=imagnet.be, geom=imagnet.geom, status=imagnet.status, msites=msites)
        magnet.mparts = imagnet.mparts
        session.add(magnet)
        session.commit()
        session.refresh(magnet)

    # ??is this needed??
    # get mpart from imagnet and update mpart
    """
    for part in mparts:
        if not magnet in part.magnets:
            part.magnets.append(magnet)
        session.refresh(part)
    """
    return magnet

def duplicate_site(session: Session, iname: str, oname: str ):
    results = query_msite(session, iname)
    for isite in results:
        print(isite)
        magnets = get_magnets(session, isite.id)

        site = MSite(name=oname, conffile="", status=MStatus.study)
        site.magnets = isite.magnets
        session.add(site)
        session.commit()
        session.refresh(site)

    # ??is this needed??
    # get mpart from imagnet and update mpart
    """
    for part in mparts:
        if not magnet in part.magnets:
            part.magnets.append(magnet)
        session.refresh(part)
    """
    return site


from typing import TYPE_CHECKING, List, Optional

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select

from .database import create_db_and_tables, engine, get_session
from .models import MPartBase, MPart, MPartCreate, MPartRead, MPartUpdate
from .models import MagnetBase, Magnet, MagnetCreate, MagnetRead, MagnetUpdate 
from .models import MSiteBase, MSite, MSiteCreate, MSiteRead, MSiteUpdate
from .models import MRecordBase, MRecord, MRecordCreate, MRecordRead, MRecordUpdate
from .models import MaterialBase, Material, MaterialCreate, MaterialRead, MaterialUpdate
from .models import MagnetReadWithMSite, MSiteReadWithMagnets
from .models import MPartReadWithMagnet
from . import crud


"""
def get_session():
    with Session(engine) as session:
        yield session
"""

itemrouter = APIRouter()

@itemrouter.post("/api/materials/", response_model=MaterialRead)
def create_material(*, session: Session = Depends(get_session), material: MaterialCreate):
    db_material = Material.from_orm(material)
    session.add(db_material)
    session.commit()
    session.refresh(db_material)
    return db_material

@itemrouter.get("/api/materials/", response_model=List[MaterialRead])
def read_materials(*, session: Session = Depends(get_session), ):
    statement = select(Material)
    materials = session.exec(statement).all()
    return materials


@itemrouter.get("/api/materials/{material_id}", response_model=MaterialBase)
def read_material(*, session: Session = Depends(get_session), material_id: int):
    material = session.get(Material, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material

# name shall be made unique
@itemrouter.get("/api/materials/name/{name}", response_model=MaterialRead)
def read_material_name(*, session: Session = Depends(get_session), name: str):
    statement = select(Material).where(Material.name == name)
    materials = session.exec(statement).one()
    return materials

@itemrouter.patch("/api/materials/{material_id}", response_model=MaterialRead)
def update_material(*, session: Session = Depends(get_session), material_id: int, material: MaterialUpdate):
    db_material = session.get(Material, material_id)
    if not db_material:
        raise HTTPException(status_code=404, detail="Material not found")
    material_data = material.dict(exclude_unset=True)
    for key, value in material_data.items():
        setattr(db_material, key, value)
    session.add(db_material)
    session.commit()
    session.refresh(db_material)
    return db_material

@itemrouter.delete("/api/materials/{material_id}")
def delete_material(*, session: Session = Depends(get_session), material_id: int):
    material = session.get(Material, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    session.delete(material)
    session.commit()
    return {"ok": True}        

####################
#
####################

@itemrouter.post("/api/mparts/", response_model=MPartRead)
def create_mpart(*, session: Session = Depends(get_session), mpart: MPartCreate):
    db_mpart = MPart.from_orm(mpart)
    session.add(db_mpart)
    session.commit()
    session.refresh(db_mpart)
    return db_mpart

@itemrouter.get("/api/mparts/", response_model=List[MPartRead])
def read_mparts(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    mparts = session.exec(select(MPart).offset(offset).limit(limit)).all()
    return mparts

@itemrouter.get("/api/mparts/{mpart_id}", response_model=MPartReadWithMagnet)
def read_mpart(*, session: Session = Depends(get_session), mpart_id: int):
    mpart = session.get(MPart, mpart_id)
    if not mpart:
        raise HTTPException(status_code=404, detail="MPart not found")
    return mpart

@itemrouter.patch("/api/mparts/{mpart_id}", response_model=MPartRead)
def update_mpart(
    *, session: Session = Depends(get_session), mpart_id: int, mpart: MPartUpdate):
    db_mpart = session.get(MPart, mpart_id)
    if not db_mpart:
        raise HTTPException(status_code=404, detail="MPart not found")
    mpart_data = mpart.dict(exclude_unset=True)
    for key, value in mpart_data.items():
        setattr(db_mpart, key, value)
    session.add(db_mpart)
    session.commit()
    session.refresh(db_mpart)
    return db_mpart

@itemrouter.delete("/api/mparts/{mpart_id}")
def delete_mpart(*, session: Session = Depends(get_session), mpart_id: int):
    mpart = session.get(MPart, mpart_id)
    if not mpart:
        raise HTTPException(status_code=404, detail="MPart not found")
    session.delete(mpart)
    session.commit()
    return {"ok": True}

####################
#
####################

@itemrouter.post("/api/magnets/", response_model=MagnetRead)
def create_magnet(*, session: Session = Depends(get_session), magnet: MagnetCreate):
    db_magnet = Magnet.from_orm(magnet)
    session.add(db_magnet)
    session.commit()
    session.refresh(db_magnet)
    return db_magnet


@itemrouter.get("/api/magnets/", response_model=List[MagnetRead])
def read_magnets(*, session: Session = Depends(get_session), ):
    magnets = session.exec(select(Magnet)).all()
    return magnets

@itemrouter.get("/api/magnets/{magnet_id}", response_model=MagnetReadWithMSite)
def read_magnet(*, session: Session = Depends(get_session), magnet_id: int):
    magnet = session.get(Magnet, magnet_id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")
    return magnet


@itemrouter.get("/api/magnet/parts/{magnet_id}", response_model=List[MPartRead])
def read_magnet_parts(*, session: Session = Depends(get_session), magnet_id: int):
    mparts = crud.get_mparts(session, magnet_id)
    if not mparts:
        raise HTTPException(status_code=404, detail="MPart not found")
    return mparts

@itemrouter.get("/api/magnet/mdata/{name}")
def read_magnet_data(*, session: Session = Depends(get_session), name: str):
    mdata = crud.get_magnet_data(session, name)
    if not mdata:
        raise HTTPException(status_code=404, detail="cannot get magnet data for %s" % name)
    return mdata

@itemrouter.get("/api/magnet/type/{name}")
def get_magnet_type(*, session: Session = Depends(get_session), name: str):
    results = crud.get_magnet_data(session, name)
    if not results:
        raise HTTPException(status_code=404, detail="cannot get type data for %s" % name)
    for mdata in results:
        return crud.get_magnet_type(session, mdata.id)
    

@itemrouter.patch("/api/magnets/{magnet_id}", response_model=MagnetRead)
def update_magnet(
    *, session: Session = Depends(get_session), magnet_id: int, magnet: MagnetUpdate):
    db_magnet = session.get(Magnet, magnet_id)
    if not db_magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")
    magnet_data = magnet.dict(exclude_unset=True)
    for key, value in magnet_data.items():
        setattr(db_magnet, key, value)
    session.add(db_magnet)
    session.commit()
    session.refresh(db_magnet)
    return db_magnet

@itemrouter.delete("/api/magnets/{magnet_id}")
def delete_magnet(*, session: Session = Depends(get_session), magnet_id: int):

    magnet = session.get(Magnet, magnet_id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")
    session.delete(magnet)
    session.commit()
    return {"ok": True}

####################
#
####################


@itemrouter.post("/api/msites/", response_model=MSiteRead)
def create_msite(*, session: Session = Depends(get_session), msite: MSiteCreate):
    db_msite = MSite.from_orm(msite)
    session.add(db_msite)
    session.commit()
    session.refresh(db_msite)
    return db_msite


@itemrouter.get("/api/msites/", response_model=List[MSiteRead])
def read_msites(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    msites = session.exec(select(MSite).offset(offset).limit(limit)).all()
    return msites

@itemrouter.get("/api/msites/{msite_id}", response_model=MSiteReadWithMagnets)
def read_msite(*, msite_id: int, session: Session = Depends(get_session)):
    msite = session.get(MSite, msite_id)
    if not msite:
        raise HTTPException(status_code=404, detail="MSite not found")
    return msite

@itemrouter.get("/api/msite/mdata/{name}")
def read_msite_data(*, session: Session = Depends(get_session), name: str):
    mdata = crud.get_msite_data(session, name)
    if not mdata:
        raise HTTPException(status_code=404, detail="cannot get magnet data for %s" % name)
    return mdata


@itemrouter.patch("/api/msites/{msite_id}", response_model=MSiteRead)
def update_msite(
    *,
    session: Session = Depends(get_session),
    msite_id: int,
    msite: MSiteUpdate,
):
    db_msite = session.get(MSite, msite_id)
    if not db_msite:
        raise HTTPException(status_code=404, detail="MSite not found")
    msite_data = msite.dict(exclude_unset=True)
    for key, value in msite_data.items():
        setattr(db_msite, key, value)
    session.add(db_msite)
    session.commit()
    session.refresh(db_msite)
    return db_msite

@itemrouter.delete("/api/msites/{msite_id}")
def delete_msite(*, session: Session = Depends(get_session), msite_id: int):
    msite = session.get(MSite, msite_id)
    if not msite:
        raise HTTPException(status_code=404, detail="MSite not found")
    session.delete(msite)
    session.commit()
    return {"ok": True}

""" 
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
"""

MSiteUpdate.update_forward_refs()
MagnetUpdate.update_forward_refs()
MPartUpdate.update_forward_refs()



from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from ... import crud
from ...database import get_session
from ...models import MPartRead
from ...models import Magnet, MagnetCreate, MagnetRead, MagnetUpdate
from ...models import MagnetReadWithMSite
from ...models import MPart, MPartUpdate
from ...models import MSite, MSiteUpdate 

router = APIRouter()


@router.post("/api/magnets/", response_model=MagnetRead)
def create_magnet(*, session: Session = Depends(get_session), magnet: MagnetCreate):
    db_magnet = Magnet.from_orm(magnet)
    session.add(db_magnet)
    session.commit()
    session.refresh(db_magnet)
    return db_magnet


@router.get("/api/magnets/", response_model=List[MagnetRead])
def read_magnets(*, session: Session = Depends(get_session), ):
    magnets = session.exec(select(Magnet)).all()
    return magnets


@router.get("/api/magnets/{magnet_id}", response_model=MagnetReadWithMSite)
def read_magnet(*, session: Session = Depends(get_session), magnet_id: int):
    magnet = session.get(Magnet, magnet_id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")
    return magnet


@router.get("/api/magnet/parts/{magnet_id}", response_model=List[MPartRead])
def read_magnet_parts(*, session: Session = Depends(get_session), magnet_id: int):
    mparts = crud.get_mparts(session, magnet_id)
    if not mparts:
        raise HTTPException(status_code=404, detail="MPart not found")
    return mparts


@router.get("/api/magnet/mdata/{name}")
def read_magnet_data(*, session: Session = Depends(get_session), name: str):
    mdata = crud.get_magnet_data(session, name)
    if not mdata:
        raise HTTPException(status_code=404, detail="cannot get magnet data for %s" % name)
    return mdata


@router.patch("/api/magnets/{magnet_id}", response_model=MagnetRead)
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


@router.delete("/api/magnets/{magnet_id}")
def delete_magnet(*, session: Session = Depends(get_session), magnet_id: int):
    magnet = session.get(Magnet, magnet_id)
    if not magnet:
        raise HTTPException(status_code=404, detail="Magnet not found")
    session.delete(magnet)
    session.commit()
    return {"ok": True}

@router.get("/api/magnet/mdata/{name}")
def read_magnet_data(*, session: Session = Depends(get_session), name: str):
    mdata = crud.get_magnet_data(session, name)
    if not mdata:
        raise HTTPException(status_code=404, detail="cannot get magnet data for %s" % name)
    return mdata

MSiteUpdate.update_forward_refs()
MagnetUpdate.update_forward_refs()
MPartUpdate.update_forward_refs()
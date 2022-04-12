from typing import TYPE_CHECKING, List, Optional

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select

from ...database import create_db_and_tables, engine, get_session
from ...models import MagnetUpdate
from ...models import MPartBase, MPart, MPartCreate, MPartRead, MPartUpdate
from ...models import MPartReadWithMagnet

router = APIRouter()


@router.post("/api/mparts/", response_model=MPartRead)
def create_mpart(*, session: Session = Depends(get_session), mpart: MPartCreate):
    db_mpart = MPart.from_orm(mpart)
    session.add(db_mpart)
    session.commit()
    session.refresh(db_mpart)
    return db_mpart

@router.get("/api/mparts/", response_model=List[MPartRead])
def read_mparts(
        *,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, lte=100),
):
    mparts = session.exec(select(MPart).offset(offset).limit(limit)).all()
    return mparts

@router.get("/api/mparts/{mpart_id}", response_model=MPartReadWithMagnet)
def read_mpart(*, session: Session = Depends(get_session), mpart_id: int):
    mpart = session.get(MPart, mpart_id)
    if not mpart:
        raise HTTPException(status_code=404, detail="MPart not found")
    return mpart

@router.patch("/api/mparts/{mpart_id}", response_model=MPartRead)
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

@router.delete("/api/mparts/{mpart_id}")
def delete_mpart(*, session: Session = Depends(get_session), mpart_id: int):
    mpart = session.get(MPart, mpart_id)
    if not mpart:
        raise HTTPException(status_code=404, detail="MPart not found")
    session.delete(mpart)
    session.commit()
    return {"ok": True}


MagnetUpdate.update_forward_refs()
MPartUpdate.update_forward_refs()
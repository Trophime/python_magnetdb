from typing import TYPE_CHECKING, List, Optional

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select

from ...database import get_session
from ...models import MagnetUpdate
from ...models import MSite, MSiteCreate, MSiteRead, MSiteUpdate
from ...models import MSiteReadWithMagnets
from ...crud import get_msite_data, get_magnet_data

router = APIRouter()


@router.post("/api/msites/", response_model=MSiteRead)
def create_msite(*, session: Session = Depends(get_session), msite: MSiteCreate):
    db_msite = MSite.from_orm(msite)
    session.add(db_msite)
    session.commit()
    session.refresh(db_msite)
    return db_msite


@router.get("/api/msites/", response_model=List[MSiteRead])
def read_msites(
        *,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, lte=100),
):
    msites = session.exec(select(MSite).offset(offset).limit(limit)).all()
    return msites


@router.get("/api/msites/{msite_id}", response_model=MSiteReadWithMagnets)
def read_msite(*, msite_id: int, session: Session = Depends(get_session)):
    msite = session.get(MSite, msite_id)
    if not msite:
        raise HTTPException(status_code=404, detail="MSite not found")
    return msite


@router.patch("/api/msites/{msite_id}", response_model=MSiteRead)
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


@router.delete("/api/msites/{msite_id}")
def delete_msite(*, session: Session = Depends(get_session), msite_id: int):
    msite = session.get(MSite, msite_id)
    if not msite:
        raise HTTPException(status_code=404, detail="MSite not found")
    session.delete(msite)
    session.commit()
    return {"ok": True}

@router.get("/api/msite/mdata/{name}")
def read_msite_data(*, session: Session = Depends(get_session), name: str):
    mdata = get_msite_data(session, name)
    if not mdata:
        raise HTTPException(status_code=404, detail="cannot get msite data for %s" % name)
    return mdata

MSiteUpdate.update_forward_refs()
MagnetUpdate.update_forward_refs()

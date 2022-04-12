from typing import TYPE_CHECKING, List, Optional

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select

from ...database import get_session
from ...models import MaterialBase, Material, MaterialCreate, MaterialRead, MaterialUpdate

router = APIRouter()


@router.post("/api/materials/", response_model=MaterialRead)
def create_material(*, session: Session = Depends(get_session), material: MaterialCreate):
    db_material = Material.from_orm(material)
    session.add(db_material)
    session.commit()
    session.refresh(db_material)
    return db_material


@router.get("/api/materials/", response_model=List[MaterialRead])
def read_materials(*, session: Session = Depends(get_session), ):
    statement = select(Material)
    materials = session.exec(statement).all()
    return materials


@router.get("/api/materials/{material_id}", response_model=MaterialBase)
def read_material(*, session: Session = Depends(get_session), material_id: int):
    material = session.get(Material, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material


# name shall be made unique
@router.get("/api/materials/name/{name}", response_model=MaterialRead)
def read_material_name(*, session: Session = Depends(get_session), name: str):
    statement = select(Material).where(Material.name == name)
    materials = session.exec(statement).one()
    return materials


@router.patch("/api/materials/{material_id}", response_model=MaterialRead)
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


@router.delete("/api/materials/{material_id}")
def delete_material(*, session: Session = Depends(get_session), material_id: int):
    material = session.get(Material, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    session.delete(material)
    session.commit()
    return {"ok": True}

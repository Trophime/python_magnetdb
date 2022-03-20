from fastapi import Depends, APIRouter, Form

from ...dependencies import get_user

router = APIRouter()


@router.get("/api/user")
def show(user=Depends(get_user('read'))):
    return user.serialize()


@router.patch("/api/user")
def update(user=Depends(get_user('read')), name: str = Form(...)):
    user.name = name
    user.save()
    return user.serialize()

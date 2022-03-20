from fastapi import Depends, APIRouter, Query, HTTPException, Form

from ....dependencies import get_user
from ....models.user import User

router = APIRouter()


@router.get("/api/admin/users")
def index(user=Depends(get_user('admin')), page: int = 1, per_page: int = Query(default=25, lte=100),
         query: str = Query(None), sort_by: str = Query(None), sort_desc: bool = Query(False)):
    users = User
    if query is not None and query.strip() != '':
        users = users.where('name', 'ilike', f'%{query}%').or_where('email', 'ilike', f'%{query}%')
    if sort_by is not None:
        users = users.order_by(sort_by, 'desc' if sort_desc else 'asc')
    users = users.paginate(per_page, page)
    return {
        "current_page": users.current_page,
        "last_page": users.last_page,
        "total": users.total,
        "items": users.serialize(),
    }


@router.get("/api/admin/users/{id}")
def show(id: int, user=Depends(get_user('admin'))):
    user = User.find(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.serialize()


@router.patch("/api/admin/users/{id}")
def update(id: int, user=Depends(get_user('admin')), name: str = Form(...), role: str = Form(...)):
    user = User.find(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = name
    user.role = role
    user.save()
    return user.serialize()

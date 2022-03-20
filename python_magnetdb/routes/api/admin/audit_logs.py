from fastapi import Depends, APIRouter, Query

from ....dependencies import get_user
from ....models.audit_log import AuditLog

router = APIRouter()


@router.get("/api/admin/audit_logs")
def index(user=Depends(get_user('admin')), page: int = 1, per_page: int = Query(default=25, lte=100),
         query: str = Query(None), sort_by: str = Query(None), sort_desc: bool = Query(False)):
    logs = AuditLog.with_('user')
    if query is not None and query.strip() != '':
        logs = logs.where('message', 'ilike', f'%{query}%')
    if sort_by is not None:
        logs = logs.order_by(sort_by, 'desc' if sort_desc else 'asc')
    logs = logs.paginate(per_page, page)
    return {
        "current_page": logs.current_page,
        "last_page": logs.last_page,
        "total": logs.total,
        "items": logs.serialize(),
    }

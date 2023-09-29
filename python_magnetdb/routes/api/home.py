from fastapi import Depends, APIRouter

from ...dependencies import get_user, get_db

router = APIRouter()


@router.get("/api/home")
def show(db=Depends(get_db)):
    sites = db.table('sites').select('status', db.raw('count(*) as count')).group_by('status').get()
    magnets = db.table('magnets').select('status', db.raw('count(*) as count')).group_by('status').get()
    users_count = db.table('users').count()
    records_count = db.table('records').count()
    return {
        'sites': sites.serialize(),
        'magnets': magnets.serialize(),
        'users_count': users_count,
        'records_count': records_count,
    }

from fastapi import Depends, APIRouter, HTTPException, Query, Form

from ...actions.generate_server_key_pairs import generate_server_key_pairs
from ...dependencies import get_user
from ...models.audit_log import AuditLog
from ...models.server import Server

router = APIRouter()


@router.get("/api/servers")
def index(user=Depends(get_user('read')), page: int = 1, per_page: int = Query(default=25, lte=100),
          query: str = Query(None), sort_by: str = Query(None), sort_desc: bool = Query(False)):
    sites = Server.where('user_id', user.id)
    if query is not None and query.strip() != '':
        sites = sites.where('name', 'ilike', f'%{query}%')
    if sort_by is not None:
        sites = sites.order_by(sort_by, 'desc' if sort_desc else 'asc')
    sites = sites.paginate(per_page, page)
    return {
        "current_page": sites.current_page,
        "last_page": sites.last_page,
        "total": sites.total,
        "items": sites.serialize(),
    }


@router.post("/api/servers")
def create(name: str = Form(...), host: str = Form(...), username: str = Form(...),
           image_directory: str = Form(...), type: str = Form(None), smp: bool = Form(None),
           multithreading: bool = Form(None), cores: int = Form(None),
           job_manager: str = Form(None), mesh_gems_directory: str = Form(None),
           user=Depends(get_user('create'))):
    private_key, public_key = generate_server_key_pairs()
    server = Server(name=name, host=host, username=username, image_directory=image_directory, private_key=private_key,
                    public_key=public_key)
    server.user().associate(user)
    if type is not None:
        server.type = type
    if smp is not None:
        server.smp = smp
    if multithreading is not None:
        server.multithreading = multithreading
    if cores is not None:
        server.cores = cores
    if job_manager is not None:
        server.job_manager = job_manager
    if mesh_gems_directory is not None:
        server.mesh_gems_directory = mesh_gems_directory
    server.save()
    AuditLog.log(user, "Server created", resource=server)
    return server.serialize()


@router.get("/api/servers/{id}")
def show(id: int, user=Depends(get_user('read'))):
    server = Server.where('user_id', user.id).find(id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server.serialize()


@router.patch("/api/servers/{id}")
def update(id: int, name: str = Form(...), host: str = Form(...), username: str = Form(...),
           image_directory: str = Form(...), type: str = Form(...), smp: bool = Form(...),
           multithreading: bool = Form(...), cores: int = Form(...),
           job_manager: str = Form(...), mesh_gems_directory: str = Form(...), user=Depends(get_user('update'))):
    server = Server.where('user_id', user.id).find(id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    server.name = name
    server.host = host
    server.username = username
    server.image_directory = image_directory
    server.type = type
    server.smp = smp
    server.multithreading = multithreading
    server.cores = cores
    server.job_manager = job_manager
    server.mesh_gems_directory = mesh_gems_directory
    server.save()
    AuditLog.log(user, "Server updated", resource=server)
    return server.serialize()


@router.delete("/api/servers/{id}")
def destroy(id: int, user=Depends(get_user('delete'))):
    server = Server.where('user_id', user.id).find(id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    server.delete()
    AuditLog.log(user, "Server deleted", resource=server)
    return server.serialize()

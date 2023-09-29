from orator import Model
from orator.orm import belongs_to


class Server(Model):
    __table__ = "servers"
    __fillable__ = ['name', 'user_id', 'username', 'host', 'private_key', 'public_key', 'image_directory', 'type',
                    'smp', 'multithreading', 'cores', 'dns', 'job_manager', 'mesh_gems_directory']
    __hidden__ = ['private_key']

    @belongs_to('user_id')
    def user(self):
        from .user import User
        return User

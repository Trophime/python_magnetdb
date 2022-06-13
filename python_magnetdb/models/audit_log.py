from orator import Model
from orator.orm import belongs_to, morph_to


class AuditLog(Model):
    __table__ = "audit_logs"
    __fillable__ = ['message', 'metadata', 'user_id', 'resource_id', 'resource_type', 'resource_name']

    @morph_to
    def resource(self):
        return

    @belongs_to('user_id')
    def user(self):
        from python_magnetdb.models.user import User
        return User

    @classmethod
    def log(cls, user, message, metadata=None, resource=None, resource_name=None):
        log = cls(message=message, metadata=metadata)
        log.user().associate(user)
        if resource is not None:
            log.resource().associate(resource)
            if hasattr(resource, 'name'):
                log.resource_name = resource.name
        if resource_name is not None:
            log.resource_name = resource_name
        log.save()
        return log

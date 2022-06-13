from orator import Model


class User(Model):
    __table__ = "users"
    __fillable__ = ['username', 'role', 'email', 'name', 'api_key']

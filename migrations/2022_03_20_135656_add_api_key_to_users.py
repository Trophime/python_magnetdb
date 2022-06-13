from orator.migrations import Migration
from uuid import uuid4 as uuid


class AddApiKeyToUsers(Migration):
    def up(self):
        with self.schema.table('users') as table:
            table.string('api_key').unique().nullable()
        for users in self.db.table('users').chunk(100):
            for user in users:
                self.db.table('users').where('id', user['id']).update(api_key=str(uuid()).replace('-', ''))
        with self.schema.table('users') as table:
            table.string('api_key').change()

    def down(self):
        with self.schema.table('users') as table:
            table.drop_column('api_key')

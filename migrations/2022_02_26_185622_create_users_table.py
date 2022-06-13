from orator.migrations import Migration


class CreateUsersTable(Migration):
    def up(self):
        with self.db.transaction():
            with self.schema.create('users') as table:
                table.big_increments('id')
                table.string('username')
                table.string('email')
                table.string('name')
                table.string('role').default('guest')
                table.timestamps()
                table.unique('username')

    def down(self):
        with self.db.transaction():
            self.schema.drop('users')

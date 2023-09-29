from orator.migrations import Migration


class CreateServersTable(Migration):
    def up(self):
        with self.db.transaction():
            with self.schema.create('servers') as table:
                table.big_increments('id')
                table.string('name')
                table.big_integer('user_id')
                table.string('username')
                table.string('host')
                table.text('private_key')
                table.text('public_key')
                table.timestamps()

    def down(self):
        with self.db.transaction():
            self.schema.drop('servers')

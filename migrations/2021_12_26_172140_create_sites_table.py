from orator.migrations import Migration


class CreateSitesTable(Migration):
    def up(self):
        with self.db.transaction():
            with self.schema.create('sites') as table:
                table.big_increments('id')
                table.string('name')
                table.long_text('description').nullable()
                table.string('status')
                table.big_integer('config_attachment_id').nullable()
                table.timestamps()

    def down(self):
        with self.db.transaction():
            self.schema.drop('sites')

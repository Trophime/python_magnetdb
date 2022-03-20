from orator.migrations import Migration


class CreateRecordsTable(Migration):
    def up(self):
        with self.db.transaction():
            with self.schema.create('records') as table:
                table.big_increments('id')
                table.string('name')
                table.long_text('description').nullable()
                table.big_integer('site_id')
                table.big_integer('attachment_id').nullable()
                table.timestamps()

    def down(self):
        with self.db.transaction():
            self.schema.drop('records')

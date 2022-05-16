from orator.migrations import Migration


class CreatePartsTable(Migration):
    def up(self):
        with self.db.transaction():
            with self.schema.create('parts') as table:
                table.big_increments('id')
                table.string('name')
                table.long_text('description').nullable()
                table.string('type')
                table.string('status')
                table.big_integer('material_id')
                table.big_integer('geometry_attachment_id').nullable()
                table.big_integer('cao_attachment_id').nullable()
                table.timestamps()

    def down(self):
        with self.db.transaction():
            self.schema.drop('parts')

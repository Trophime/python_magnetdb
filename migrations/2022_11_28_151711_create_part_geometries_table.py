from orator.migrations import Migration


class CreatePartGeometriesTable(Migration):
    def up(self):
        with self.db.transaction():
            with self.schema.create('part_geometries') as table:
                table.big_increments('id')
                table.big_integer('part_id')
                table.string('type')
                table.big_integer('attachment_id')
                table.timestamps()

    def down(self):
        with self.db.transaction():
            self.schema.drop('part_geometries')

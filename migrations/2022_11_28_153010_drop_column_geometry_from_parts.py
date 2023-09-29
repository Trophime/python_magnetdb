from orator.migrations import Migration


class DropColumnGeometryFromParts(Migration):
    def up(self):
        with self.schema.table('parts') as table:
            table.drop_column('geometry_attachment_id')

    def down(self):
        with self.schema.table('parts') as table:
            table.big_integer('geometry_attachment_id').nullable()

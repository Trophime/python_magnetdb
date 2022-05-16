from orator.migrations import Migration


class AddDesignOfficeAndGeometryAttachmentToMagnets(Migration):
    def up(self):
        with self.schema.table('magnets') as table:
            table.string('design_office_reference').nullable()
            table.big_integer('geometry_attachment_id').nullable()

    def down(self):
        with self.schema.table('magnets') as table:
            table.drop_column('design_office_reference')
            table.drop_column('geometry_attachment_id')

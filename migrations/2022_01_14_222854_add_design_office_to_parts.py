from orator.migrations import Migration


class AddDesignOfficeToParts(Migration):
    def up(self):
        with self.schema.table('parts') as table:
            table.string('design_office_reference').nullable()

    def down(self):
        with self.schema.table('parts') as table:
            table.drop_column('design_office_reference')

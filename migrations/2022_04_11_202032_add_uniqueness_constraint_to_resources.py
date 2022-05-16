from orator.migrations import Migration


class AddUniquenessConstraintToResources(Migration):
    def up(self):
        with self.schema.table('magnets') as table:
            table.unique('name')
        with self.schema.table('parts') as table:
            table.unique('name')
        with self.schema.table('sites') as table:
            table.unique('name')

    def down(self):
        with self.schema.table('magnets') as table:
            table.drop_unique('magnets_name_unique')
        with self.schema.table('parts') as table:
            table.drop_unique('parts_name_unique')
        with self.schema.table('sites') as table:
            table.drop_unique('sites_name_unique')

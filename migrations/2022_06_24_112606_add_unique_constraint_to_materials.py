from orator.migrations import Migration


class AddUniqueConstraintToMaterials(Migration):

    def up(self):
        with self.schema.table('materials') as table:
            table.unique('name')

    def down(self):
        with self.schema.table('materials') as table:
            table.drop_unique('materials_name_unique')

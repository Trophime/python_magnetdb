from orator.migrations import Migration


class RenameShadeToNuanceInMaterials(Migration):
    def up(self):
        with self.schema.table('materials') as table:
            table.rename_column('shade', 'nuance')

    def down(self):
        with self.schema.table('materials') as table:
            table.rename_column('nuance', 'shade')

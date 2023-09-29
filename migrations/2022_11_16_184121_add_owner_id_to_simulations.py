from orator.migrations import Migration


class AddOwnerIdToSimulations(Migration):

    def up(self):
        with self.schema.table('simulations') as table:
            table.big_integer('owner_id')


    def down(self):
        with self.schema.table('simulations') as table:
            table.drop_column('owner_id')

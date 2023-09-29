from orator.migrations import Migration


class AddSetupStateToSimulations(Migration):

    def up(self):
        with self.schema.table('simulations') as table:
            table.json('setup_state').nullable()


    def down(self):
        with self.schema.table('simulations') as table:
            table.drop_column('setup_state')

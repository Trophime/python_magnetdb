from orator.migrations import Migration


class AddStaticAndNonLinearToSimulations(Migration):
    def up(self):
        with self.schema.table('simulations') as table:
            table.boolean('static').nullable()
            table.boolean('non_linear').nullable()

    def down(self):
        with self.schema.table('simulations') as table:
            table.drop_column('static')
            table.drop_column('non_linear')

from orator.migrations import Migration


class CreateSimulationsTable(Migration):
    def up(self):
        with self.db.transaction():
            with self.schema.create('simulations') as table:
                table.big_increments('id')
                table.text('status').nullable()
                table.text('resource_type').nullable()
                table.big_integer('resource_id').nullable()
                table.text('method').nullable()
                table.text('model').nullable()
                table.text('geometry').nullable()
                table.text('cooling').nullable()
                table.big_integer('result_attachment_id').nullable()
                table.timestamps()

    def down(self):
        with self.db.transaction():
            self.schema.drop('simulations')

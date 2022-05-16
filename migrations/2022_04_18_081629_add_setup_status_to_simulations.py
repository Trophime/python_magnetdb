from orator.migrations import Migration


class AddSetupStatusToSimulations(Migration):
    def up(self):
        with self.schema.table('simulations') as table:
            table.rename_column('result_attachment_id', 'output_attachment_id')
            table.big_integer('setup_output_attachment_id').nullable()
            table.text('status').default('pending').change()
            table.text('setup_status').default('pending')

    def down(self):
        with self.schema.table('simulations') as table:
            table.rename_column('output_attachment_id', 'result_attachment_id')
            table.text('status').nullable().change()
            table.drop_column('setup_output_attachment_id')
            table.drop_column('setup_status')

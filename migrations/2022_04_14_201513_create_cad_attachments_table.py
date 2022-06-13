from orator.migrations import Migration


class CreateCadAttachmentsTable(Migration):
    def up(self):
        with self.db.transaction():
            with self.schema.create('cad_attachments') as table:
                table.big_increments('id')
                table.big_integer('attachment_id')
                table.text('resource_type')
                table.big_integer('resource_id')
                table.timestamps()

    def down(self):
        with self.db.transaction():
            self.schema.drop('cad_attachments')

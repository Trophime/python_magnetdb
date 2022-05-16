from orator.migrations import Migration


class CreateAttachmentsTable(Migration):
    def up(self):
        with self.db.transaction():
            with self.schema.create('storage_attachments') as table:
                table.big_increments('id')
                table.string('filename').nullable()
                table.string('content_type').nullable()
                table.string('key')
                table.timestamps()

    def down(self):
        with self.db.transaction():
            self.schema.drop('storage_attachments')

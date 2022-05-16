from orator.migrations import Migration


class CreateAuditLogsTable(Migration):
    def up(self):
        with self.db.transaction():
            with self.schema.create('audit_logs') as table:
                table.big_increments('id')
                table.long_text('message')
                table.json('metadata').nullable()
                table.big_integer('user_id')
                table.big_integer('resource_id').nullable()
                table.text('resource_type').nullable()
                table.text('resource_name').nullable()
                table.timestamps()

    def down(self):
        with self.db.transaction():
            self.schema.drop('audit_logs')

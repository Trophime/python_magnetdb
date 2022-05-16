from orator.migrations import Migration


class CreateMagnetsTable(Migration):
    def up(self):
        with self.db.transaction():
            with self.schema.create('magnets') as table:
                table.big_increments('id')
                table.string('name')
                table.long_text('description').nullable()
                table.string('status')
                table.big_integer('cao_attachment_id').nullable()
                table.timestamps()
            with self.schema.create('magnet_parts') as table:
                table.big_increments('id')
                table.big_integer('magnet_id')
                table.big_integer('part_id')
                table.timestamp('commissioned_at')
                table.timestamp('decommissioned_at').nullable()
                table.timestamps()
            with self.schema.create('site_magnets') as table:
                table.big_increments('id')
                table.big_integer('magnet_id')
                table.big_integer('site_id')
                table.timestamp('commissioned_at')
                table.timestamp('decommissioned_at').nullable()
                table.timestamps()

    def down(self):
        with self.db.transaction():
            self.schema.drop('site_magnets')
            self.schema.drop('magnet_parts')
            self.schema.drop('magnets')

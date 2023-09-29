from orator.migrations import Migration


class DropDnsColumnFromServers(Migration):
    def up(self):
        with self.schema.table('servers') as table:
            table.drop_column('dns')

    def down(self):
        with self.schema.table('servers') as table:
            table.string('dns').default('localhost')

from orator.migrations import Migration


class AddImageDirectoryToServers(Migration):
    def up(self):
        with self.schema.table('servers') as table:
            table.string('image_directory')


    def down(self):
        with self.schema.table('servers') as table:
            table.drop_column('image_directory')

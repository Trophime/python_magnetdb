from orator.migrations import Migration


class AddNodespecToServersTable(Migration):
    def up(self):
        with self.schema.table('servers') as table:
            table.string('type').default('compute')
            table.boolean('smp').default(True)
            table.boolean('multithreading').default(True)
            table.integer('cores').default(1)
            table.string('dns').default('localhost')
            table.string('job_manager').default('none')
            table.string('mesh_gems_directory').default('/opt/MeshGems')

    def down(self):
        with self.schema.table('servers') as table:
            table.drop_column('type')
            table.drop_column('smp')
            table.drop_column('multithreading')
            table.drop_column('cores')
            table.drop_column('dns')
            table.drop_column('job_manager')
            table.drop_column('mesh_gems_directory')

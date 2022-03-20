from orator.migrations import Migration


class CreateMaterialsTable(Migration):
    def up(self):
        with self.db.transaction():
            with self.schema.create('materials') as table:
                table.big_increments('id')
                table.string('name')
                table.string('shade').nullable()
                table.long_text('description').nullable()
                table.float('t_ref').default(20)
                table.float('volumic_mass').default(0)
                table.float('alpha').default(0)
                table.float('specific_heat').default(0)
                table.float('electrical_conductivity').default(0)
                table.float('thermal_conductivity').default(0)
                table.float('magnet_permeability').default(0)
                table.float('young').default(0)
                table.float('poisson').default(0)
                table.float('expansion_coefficient').default(0)
                table.float('rpe')
                table.timestamps()

    def down(self):
        with self.db.transaction():
            self.schema.drop('materials')

from orator.migrations import Migration


class CreateSimulationCurrentsTable(Migration):
    def up(self):
        with self.db.transaction():
            with self.schema.create('simulation_currents') as table:
                table.big_increments('id')
                table.big_integer('simulation_id')
                table.big_integer('magnet_id')
                table.float('value')
                table.timestamps()

    def down(self):
        with self.db.transaction():
            self.schema.drop('simulation_currents')

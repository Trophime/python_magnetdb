from orator.migrations import Migration


class BackfillPartGeometries(Migration):
    def up(self):
        with self.db.transaction():
            for part in self.db.table('parts').get():
                self.db.table('part_geometries').insert({
                    'type': 'default',
                    'part_id': part.id,
                    'attachment_id': part.geometry_attachment_id
                })

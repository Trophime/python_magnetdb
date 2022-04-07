from datetime import datetime
from uuid import uuid4

from orator import DatabaseManager, Schema, Model
from os import getenv, path, listdir

from .models.attachment import Attachment
from .models.magnet import Magnet
from .models.magnet_part import MagnetPart
from .models.material import Material
from .models.part import Part
from .models.record import Record
from .models.site import Site
from .models.site_magnet import SiteMagnet
from .storage import s3_client, s3_bucket

db = DatabaseManager({
    'postgres': {
        'driver': 'postgres',
        'host': getenv('DATABASE_HOST') or 'localhost',
        'database': getenv('DATABASE_NAME') or 'magnetdb',
        'user': getenv('DATABASE_USER') or 'magnetdb',
        'password': getenv('DATABASE_PASSWORD') or 'magnetdb',
        'prefix': ''
    }
})
schema = Schema(db)
Model.set_connection_resolver(db)

data_directory = getenv('DATA_DIR')


def upload_attachment(file: str) -> Attachment:
    attachment = Attachment.create({
        "key": str(uuid4()),
        "filename": path.basename(file),
        "content_type": 'text/tsv',
    })
    s3_client.fput_object(s3_bucket, attachment.key, file, content_type=attachment.content_type)
    return attachment


def create_material(obj):
    return Material.create(obj)


def create_part(obj):
    material = obj.pop('material', None)
    geometry = obj.pop('geometry', None)
    cao = obj.pop('cao', None)
    part = Part(obj)
    if material is not None:
        part.material().associate(material)
    if geometry is not None:
        part.geometry().associate(upload_attachment(path.join(data_directory, 'geometries', f"{geometry}.yaml")))
    if cao is not None:
        part.cao().associate(upload_attachment(path.join(data_directory, 'cad', f"{cao}.xao")))
    part.save()
    return part


def create_site(obj):
    config = obj.pop('config', None)
    site = Site(obj)
    if config is not None:
        site.config().associate(upload_attachment(path.join(data_directory, 'cfg', f"{config}.cfg")))
    site.save()
    return site


def create_magnet(obj):
    site = obj.pop('site', None)
    parts = obj.pop('parts', None)
    geometry = obj.pop('geometry', None)
    cao = obj.pop('cao', None)
    magnet = Magnet(obj)
    if geometry is not None:
        magnet.geometry().associate(upload_attachment(path.join(data_directory, 'geometries', f"{geometry}.yaml")))
    if cao is not None:
        magnet.cao().associate(upload_attachment(path.join(data_directory, 'cad', f"{cao}.xao")))
    magnet.save()
    if site is not None:
        site_magnet = SiteMagnet(commissioned_at=datetime.now())
        site_magnet.site().associate(site)
        magnet.site_magnets().save(site_magnet)
    if parts is not None:
        def generate_part(part):
            magnet_part = MagnetPart(commissioned_at=datetime.now())
            magnet_part.part().associate(part)
            return magnet_part
        magnet.magnet_parts().save_many(map(generate_part, parts))
    return magnet


def create_record(file, site):
    record = Record(name=path.basename(file))
    record.attachment().associate(upload_attachment(file))
    record.site().associate(site)
    record.save()
    return record


MA15101601 = create_material({
    'name': 'MA15101601',
    'description': 'H1',
    'nuance': 'CuAg5.5',
    't_ref': 293,
    'volumic_mass': 9e+3,
    'specific_heat': 0,
    'alpha': 3.6e-3,
    'electrical_conductivity': 52.4e+6,
    'thermal_conductivity': 380,
    'magnet_permeability': 1,
    'young': 117e+9,
    'poisson': 0.33,
    'expansion_coefficient': 18e-6,
    'rpe': 481,
})
MA15061703 = create_material({
    'name': 'MA15061703',
    'description': 'H2',
    'nuance': 'CuAg5.5',
    't_ref': 293,
    'volumic_mass': 9e+3,
    'specific_heat': 0,
    'alpha': 3.6e-3,
    'electrical_conductivity': 53.3e+6,
    'thermal_conductivity': 380,
    'magnet_permeability': 1,
    'young': 117e+9,
    'poisson': 0.33,
    'expansion_coefficient': 18e-6,
    'rpe': 482,
})
MA15061801 = create_material({
    'name': 'MA15061801',
    'description': 'H3',
    'nuance': 'CuAg5.5',
    't_ref': 293,
    'volumic_mass': 9e+3,
    'specific_heat': 0,
    'alpha': 3.6e-3,
    'electrical_conductivity': 52.6e+6,
    'thermal_conductivity': 380,
    'magnet_permeability': 1,
    'young': 117e+9,
    'poisson': 0.33,
    'expansion_coefficient': 18e-6,
    'rpe': 496,
})
MA15100501 = create_material({
    'name': 'MA15100501',
    'description': 'H4',
    'nuance': 'CuAg5.5',
    't_ref': 293,
    'volumic_mass': 9e+3,
    'specific_heat': 0,
    'alpha': 3.6e-3,
    'electrical_conductivity': 52.8e+6,
    'thermal_conductivity': 380,
    'magnet_permeability': 1,
    'young': 117e+9,
    'poisson': 0.33,
    'expansion_coefficient': 18e-6,
    'rpe': 508,
})
MA15101501 = create_material({
    'name': 'MA15101501',
    'description': 'H5',
    'nuance': 'CuAg5.5',
    't_ref': 293,
    'volumic_mass': 9e+3,
    'specific_heat': 0,
    'alpha': 3.6e-3,
    'electrical_conductivity': 53.1e+6,
    'thermal_conductivity': 380,
    'magnet_permeability': 1,
    'young': 117e+9,
    'poisson': 0.33,
    'expansion_coefficient': 18e-6,
    'rpe': 506,
})
MA18060101 = create_material({
    'name': 'MA18060101',
    'description': 'H6',
    'nuance': 'CuAg5.5',
    't_ref': 293,
    'volumic_mass': 9e+3,
    'specific_heat': 0,
    'alpha': 3.6e-3,
    'electrical_conductivity': 53.2e+6,
    'thermal_conductivity': 380,
    'magnet_permeability': 1,
    'young': 117e+9,
    'poisson': 0.33,
    'expansion_coefficient': 18e-6,
    'rpe': 512,
})
MA18012501 = create_material({
    'name': 'MA18012501',
    'description': 'H7',
    'nuance': 'CuAg5.5',
    't_ref': 293,
    'volumic_mass': 9e+3,
    'specific_heat': 0,
    'alpha': 3.6e-3,
    'electrical_conductivity': 53.1e+6,
    'thermal_conductivity': 380,
    'magnet_permeability': 1,
    'young': 117e+9,
    'poisson': 0.33,
    'expansion_coefficient': 18e-6,
    'rpe': 500,
})
MA18051801 = create_material({
    'name': 'MA18051801',
    'description': 'H8',
    'nuance': 'CuAg5.5',
    't_ref': 293,
    'volumic_mass': 9e+3,
    'specific_heat': 0,
    'alpha': 3.6e-3,
    'electrical_conductivity': 51.9e+6,
    'thermal_conductivity': 380,
    'magnet_permeability': 1,
    'young': 117e+9,
    'poisson': 0.33,
    'expansion_coefficient': 18e-6,
    'rpe': 512,
})
MA18101201 = create_material({
    'name': 'MA18101201',
    'description': 'H9',
    'nuance': 'CuAg5.5',
    't_ref': 293,
    'volumic_mass': 9e+3,
    'specific_heat': 0,
    'alpha': 3.6e-3,
    'electrical_conductivity': 53.7e+6,
    'thermal_conductivity': 380,
    'magnet_permeability': 1,
    'young': 117e+9,
    'poisson': 0.33,
    'expansion_coefficient': 18e-6,
    'rpe': 500,
})
MA19012101 = create_material({
    'name': 'MA19012101',
    'description': 'H11',
    'nuance': 'CuAg5.5',
    't_ref': 293,
    'volumic_mass': 9e+3,
    'specific_heat': 0,
    'alpha': 3.6e-3,
    'electrical_conductivity': 53.8e+6,
    'thermal_conductivity': 380,
    'magnet_permeability': 1,
    'young': 117e+9,
    'poisson': 0.33,
    'expansion_coefficient': 18e-6,
    'rpe': 500,
})
MA19011601 = create_material({
    'name': 'MA19011601',
    'description': 'H12',
    'nuance': 'CuAg5.5',
    't_ref': 293,
    'volumic_mass': 9e+3,
    'specific_heat': 0,
    'alpha': 3.6e-3,
    'electrical_conductivity': 53.2e+6,
    'thermal_conductivity': 380,
    'magnet_permeability': 1,
    'young': 117e+9,
    'poisson': 0.33,
    'expansion_coefficient': 18e-6,
    'rpe': 500,
})
MA10061702 = create_material({
    'name': 'MA10061702',
    'description': 'H13',
    'nuance': 'CuCrZr',
    't_ref': 293,
    'volumic_mass': 9e+3,
    'specific_heat': 0,
    'alpha': 3.4e-3,
    'electrical_conductivity': 46.5e+6,
    'thermal_conductivity': 380,
    'magnet_permeability': 1,
    'young': 117e+9,
    'poisson': 0.33,
    'expansion_coefficient': 18e-6,
    'rpe': 366,
})
MA10061703 = create_material({
    'name': 'MA10061703',
    'description': 'H14',
    'nuance': 'CuCrZr',
    't_ref': 293,
    'volumic_mass': 9e+3,
    'specific_heat': 0,
    'alpha': 3.4e-3,
    'electrical_conductivity': 50.25e+6,
    'thermal_conductivity': 380,
    'magnet_permeability': 1,
    'young': 117e+9,
    'poisson': 0.33,
    'expansion_coefficient': 18e-6,
    'rpe': 373,
})
MAT1_RING = create_material({
    'name': '',
    'description': 'R1, R2',
    'nuance': 'unknow',
    't_ref': 293,
    'volumic_mass': 9e+3,
    'specific_heat': 0,
    'alpha': 3.4e-3,
    'electrical_conductivity': 41e+6,
    'thermal_conductivity': 320,
    'magnet_permeability': 1,
    'young': 131e+9,
    'poisson': 0.3,
    'expansion_coefficient': 17e-6,
    'rpe': 0,
})
MAT2_RING = create_material({
    'name': 'MAT2_RING',
    'description': 'R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13',
    'nuance': 'unknow',
    't_ref': 293,
    'volumic_mass': 9e+3,
    'specific_heat': 0,
    'alpha': 3.4e-3,
    'electrical_conductivity': 50e+6,
    'thermal_conductivity': 320,
    'magnet_permeability': 1,
    'young': 131e+9,
    'poisson': 0.3,
    'expansion_coefficient': 17e-6,
    'rpe': 0,
})
MAT_LEAD = create_material({
    'name': 'MAT_LEAD',
    'description': 'il1 ol2',
    'nuance': 'unknow',
    't_ref': 293,
    'volumic_mass': 9e+3,
    'specific_heat': 0,
    'alpha': 3.4e-3,
    'electrical_conductivity': 58.0e+6,
    'thermal_conductivity': 390,
    'magnet_permeability': 1,
    'young': 131e+9,
    'poisson': 0.3,
    'expansion_coefficient': 17e-6,
    'rpe': 0,
})
MAT_ISOLANT = create_material({
    'name': 'MAT_ISOLANT',
    'description': None,
    'nuance': 'unknow',
    't_ref': 20,
    'volumic_mass': 2e+3,
    'specific_heat': 0,
    'alpha': 0,
    'electrical_conductivity': 0,
    'thermal_conductivity': 1.2,
    'magnet_permeability': 1,
    'young': 2.1e9,
    'poisson': 0.21,
    'expansion_coefficient': 9e-6,
    'rpe': 0,
})


H15101601 = create_part({
    'name': 'H15101601',
    'type': 'helix',
    'status': 'in_operation',
    'material': MA15101601,
    'geometry': 'HL-31_H1',
    'cao': 'HL-31_H1',
})
H15061703 = create_part({
    'name': 'H15061703',
    'type': 'helix',
    'status': 'in_operation',
    'material': MA15061703,
    'geometry': 'HL-31_H2',
    'cao': 'HL-31_H2',
})
H15061801 = create_part({
    'name': 'H15061801',
    'type': 'helix',
    'status': 'in_operation',
    'material': MA15061801,
    'geometry': 'HL-31_H3',
    'cao': 'HL-31_H3',
})
M19061901_R1 = create_part({
    'name': 'M19061901_R1',
    'type': 'ring',
    'status': 'in_operation',
    'material': MAT1_RING,
    'geometry': 'HL-31_H4',
    'cao': 'HL-31_H4',
})
M19061901_R2 = create_part({
    'name': 'M19061901_R2',
    'type': 'ring',
    'status': 'in_operation',
    'material': MAT1_RING,
    'geometry': 'HL-31_H5',
    'cao': 'HL-31_H5',
})
M19061901_iL1 = create_part({
    'name': 'M19061901_iL1',
    'type': 'lead',
    'status': 'in_operation',
    'material': MAT_LEAD,
    'geometry': 'HL-31_H6',
    'cao': 'HL-31_H6',
})
M19061901_oL2 = create_part({
    'name': 'M19061901_oL2',
    'type': 'lead',
    'status': 'in_operation',
    'material': MAT_LEAD,
    'geometry': 'HL-31_H7',
    'cao': 'HL-31_H7',
})

MAT_TEST1 = create_material({
    'name': 'MAT_TEST1',
    'description': 'R1, R2',
    'nuance': 'Cu5Ag5,08',
    't_ref': 293,
    'volumic_mass': 9e+3,
    'specific_heat': 0,
    'alpha': 3.6e-3,
    'electrical_conductivity': 52.4e+6,
    'thermal_conductivity': 380,
    'magnet_permeability': 1,
    'young': 117e+9,
    'poisson': 0.33,
    'expansion_coefficient': 18e-6,
    'rpe': 481,
})
MAT_TEST2 = create_material({
    'name': 'MAT_TEST2',
    'description': 'R1, R2',
    'nuance': 'Cu5Ag5,08',
    't_ref': 293,
    'volumic_mass': 9e+3,
    'specific_heat': 0,
    'alpha': 3.6e-3,
    'electrical_conductivity': 53.3e+6,
    'thermal_conductivity': 380,
    'magnet_permeability': 1,
    'young': 117e+9,
    'poisson': 0.33,
    'expansion_coefficient': 18e-6,
    'rpe': 482,
})

HLtestH1 = create_part({
    'name': 'HL-34_H1',
    'type': 'helix',
    'design_office_reference': 'HL-34-001-A',
    'status': 'in_operation',
    'material': MAT_TEST1,
    'geometry': 'HL-31_H1',
})
HLtestH2 = create_part({
    'name': 'HL-34_H2',
    'type': 'helix',
    'design_office_reference': 'HL-34-001-A',
    'status': 'in_operation',
    'material': MAT_TEST2,
    'geometry': 'HL-31_H2',
})
HLtestR1 = create_part({
    'name': 'Ring-H1H2',
    'type': 'ring',
    'design_office_reference': 'HL-34-001-A',
    'status': 'in_operation',
    'material': MAT_TEST2,
    'geometry': 'Ring-H1H2',
})

MTest = create_site({
    'name': 'MTest',
    'status': 'in_operation',
    'config': 'HL-test2-cfpdes-thelec-Axi-sim',
})
MTest2 = create_site({
    'name': 'MTest2',
    'status': 'defunct',
    'config': 'HL-test2-cfpdes-thelec-Axi-sim',
})
M10 = create_site({
    'name': 'M10',
    'status': 'in_operation',
    'config': 'HL-test2-cfpdes-thelec-Axi-sim',
})


HLtest = create_magnet({
    'name': 'HL-test',
    'status': 'in_operation',
    'site': MTest,
    'parts': [HLtestH1, HLtestH2, HLtestR1],
    'geometry': 'test',
    'cao': 'HL-31',
    'design_office_reference': 'HL-34-001-A'
})
RINGtest = create_magnet({
    'name': 'RING-test',
    'status': 'in_operation',
    'site': MTest,
    'parts': [M19061901_R1, M19061901_R2],
    'geometry': 'test',
    'cao': 'HL-31',
})
LEADtest = create_magnet({
    'name': 'LEAD-test',
    'status': 'in_operation',
    'site': M10,
    'parts': [M19061901_iL1, M19061901_oL2],
    'geometry': 'test',
    'cao': 'HL-31',
})

for file in listdir(path.join(data_directory, 'mrecords')):
    create_record(path.join(data_directory, 'mrecords', file), M10)

"""
Create a basic magnetdb
"""

from datetime import datetime
from uuid import uuid4

from os import getenv, path, listdir
from orator import DatabaseManager, Schema, Model

from .models.attachment import Attachment
from .models.cad_attachment import CadAttachment
from .models.magnet import Magnet
from .models.magnet_part import MagnetPart
from .models.material import Material
from .models.part import Part
from .models.site import Site
from .models.site_magnet import SiteMagnet
from .storage import s3_client, s3_bucket

from .crud import upload_attachment, extract_date_from_filename
from .crud import create_material, create_part, create_site, create_magnet, create_record
from .crud import query_part, query_material

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


with Model.get_connection_resolver().transaction():
    # Get parts from previous defs

    M9_M19020601 = query_site('M9_M19020601')
    HTS = create_material({
    'name': "HTS",
        'nuance': "HTS",
        't_ref': 293,
        'volumic_mass': 9e+3,
        'specific_heat': 380,
        'alpha': 3.6e-3,
        'electrical_conductivity': 1.e+10,
        'thermal_conductivity': 360,
        'magnet_permeability': 1,
        'young': 127e+9,
        'poisson': 0.335,
        'expansion_coefficient': 18e-6,
        'rpe': 481000000.0
    })

    NOUGAT = create_part({
        'name': 'Nougat',
        'type': 'supra',
        'geometry': 'Nougat',
        'status': 'in_study',
        'material': HTS
    })

    MNOUGAT = create_magnet({
        'name': "Nougat",
        'parts': [NOUGAT],
        'status': 'in_study',
        'design_office_reference': 'Nougat',
        'site': M9_M19020601
    })
    
    

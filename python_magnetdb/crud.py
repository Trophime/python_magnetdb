"""
Basic crud methods
"""

import re
from datetime import datetime
from os import path, getenv
from uuid import uuid4

from python_magnetdb.models.part_geometry import PartGeometry
from .models.attachment import Attachment
from .models.cad_attachment import CadAttachment
from .models.magnet import Magnet
from .models.magnet_part import MagnetPart
from .models.material import Material
from .models.part import Part
from .models.record import Record
from .models.site import Site
from .models.site_magnet import SiteMagnet
from .storage import s3_client, s3_bucket

data_directory = getenv('DATA_DIR')


def upload_attachment(file: str) -> Attachment:
    """upload file as attachment in s3_bucket"""
    attachment = Attachment.create({
        "key": str(uuid4()),
        "filename": path.basename(file),
        "content_type": 'text/tsv',
    })
    s3_client.fput_object(s3_bucket, attachment.key, file, content_type=attachment.content_type)
    return attachment


def create_material(obj):
    """create material"""
    return Material.create(obj)


def create_part(obj):
    """create part"""
    material = obj.pop('material', None)
    geometry = obj.pop('geometry', None)
    cad = obj.pop('cad', None)
    part = Part(obj)
    if material is not None:
        part.material().associate(material)
    part.save()
    if geometry is not None:
        part_geometry = PartGeometry(type='default')
        part_geometry.part().associate(part)
        part_geometry.attachment().associate(
            upload_attachment(path.join(data_directory, 'geometries', f"{geometry}.yaml"))
        )
        part.geometries().save_many([part_geometry])
    if cad is not None:
        def generate_cad_attachment(file):
            cad_attachment = CadAttachment()
            cad_attachment.resource().associate(part)
            cad_attachment.attachment().associate(upload_attachment(path.join(data_directory, 'cad', file)))
            return cad_attachment
        part.cad().save_many(map(generate_cad_attachment, [f"{cad}.xao", f"{cad}.brep"]))
    return part


def create_site(obj):
    """create site"""
    config = obj.pop('config', None)
    site = Site(obj)
    if config is not None:
        site.config().associate(upload_attachment(path.join(data_directory, 'conf', f"{config}")))
    site.save()
    return site


def create_magnet(obj):
    """create magnet"""
    site = obj.pop('site', None)
    parts = obj.pop('parts', None)
    geometry = obj.pop('geometry', None)
    cad = obj.pop('cad', None)
    magnet = Magnet(obj)
    if geometry is not None:
        magnet.geometry().associate(upload_attachment(path.join(data_directory, 'geometries', f"{geometry}.yaml")))
    magnet.save()
    if cad is not None:
        def generate_cad_attachment(file):
            cad_attachment = CadAttachment()
            cad_attachment.resource().associate(magnet)
            cad_attachment.attachment().associate(upload_attachment(path.join(data_directory, 'cad', file)))
            return cad_attachment
        magnet.cad().save_many(map(generate_cad_attachment, [f"{cad}.xao", f"{cad}.brep"]))
    if site is not None:
        site_magnet = SiteMagnet(commissioned_at=datetime.now())
        site_magnet.site().associate(site)
        magnet.site_magnets().save(site_magnet)
    if parts is not None:
        def generate_part(part):
            magnet_part = MagnetPart(commissioned_at=datetime.now())
            print('part:', part.name)
            magnet_part.part().associate(part)
            return magnet_part
        magnet.magnet_parts().save_many(map(generate_part, parts))
    return magnet

def extract_date_from_filename(filename):
    for match in re.finditer(r".+_(\d{4}).(\d{2}).(\d{2})---(\d{2}):(\d{2}):(\d{2}).+", filename):
        return datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)),
                        int(match.group(4)), int(match.group(5)), int(match.group(6)))
    return None

def create_record(obj):
    """create a record from file for site"""

    file = obj.pop('file', None)
    site = obj.pop('site', None)
    if file is not None and site is not None:
        print(f'{data_directory}/mrecords/{file}')
        print(f"{path.basename(path.join(data_directory, 'mrecords', file))}")
        created_at = extract_date_from_filename(path.basename(path.join(data_directory, 'mrecords', file)))
        print(f'created_at={created_at}')
        if created_at is None:
            created_at = datetime.now()
        record = Record(name=path.basename(path.join(data_directory, 'mrecords', file)), created_at=created_at)
        record.attachment().associate(upload_attachment(path.join(data_directory, 'mrecords', file)))
        record.site().associate(site)
        record.save()
        return record

def query_part(name: str):
    """search a part object by name"""
    selected = db.table('parts').where('name', name).get()
    if selected.count() != 1:
        raise(f'parts[name={name} returns more than one object ({selected.count()})')
    elif selected.count() == 0:
        print(f'parts[name={name} no such object)')
        return None
    else:
        return Part.where('name', name).first()

def query_material(name: str):
    """search a material object by name"""
    selected = db.table('materials').where('name', name).get()
    if selected.count() != 1:
        raise(f'materials[name={name} returns more than one object ({selected.count()})')
    elif selected.count() == 0:
        print(f'materials[name={name} no such object)')
        return None
    else:
        return Material.where('name', name).first()

def query_site(name: str):
    """search a site object by name"""
    # print(f"looking for part=={name}")
    selected = db.table('sites').where('name', name).get()
    if selected.count() != 1:
        raise(f'sites[name={name} returns more than one object ({selected.count()})')
    elif selected.count() == 0:
        print(f'sites[name={name} no such object)')
        return None
    else:
        return Site.where('name', name).first()

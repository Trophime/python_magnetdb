import json
import os
import shutil

from python_magnetdb.actions.generate_simulation_config import generate_magnet_config
from python_magnetdb.models.magnet import Magnet


def mkdir(dir):
    try:
        os.mkdir(dir)
    except FileExistsError:
        pass


def generate_magnet_directory(magnet_id, directory):
    magnet = Magnet.with_('magnet_parts.part.geometry', 'magnet_parts.part.cad.attachment', 'geometry',
                          'magnet_parts.part.material', 'site_magnets.site', 'cad.attachment').find(magnet_id)
    mkdir(f"{directory}/data")
    mkdir(f"{directory}/data/geometries")
    mkdir(f"{directory}/data/cad")
    shutil.copyfile(f"{os.getcwd()}/flow_params.json", f"{directory}/flow_params.json")
    if magnet.geometry:
        magnet.geometry.download(f"{directory}/data/geometries/{magnet.geometry.filename}")
    for magnet_part in magnet.magnet_parts:
        if not magnet_part.active:
            continue
        if magnet_part.part.geometry:
            magnet_part.part.geometry.download(f"{directory}/data/geometries/{magnet_part.part.geometry.filename}")
        if magnet_part.part.cad:
            for cad in magnet_part.part.cad:
                cad.attachment.download(f"{directory}/data/cad/{cad.attachment.filename}")
    with open(f"{directory}/config.json", "w+") as file:
        config = generate_magnet_config(magnet_id)
        file.write(json.dumps(config))
        return config

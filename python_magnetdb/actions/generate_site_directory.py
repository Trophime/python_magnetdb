import json
import os
import shutil

from python_magnetdb.actions.generate_simulation_config import generate_magnet_config
from python_magnetdb.models.site import Site


def mkdir(dir):
    try:
        os.mkdir(dir)
    except FileExistsError:
        pass


def generate_site_directory(site_id, directory):
    site = Site.with_(
        "site_magnets.magnet.magnet_parts.part.geometries.attachment",
        "site_magnets.magnet.magnet_parts.part.cad.attachment",
        "site_magnets.magnet.geometry",
        "site_magnets.magnet.magnet_parts.part.material",
        "site_magnets.magnet.cad.attachment",
    ).find(site_id)
    mkdir(f"{directory}/data")
    mkdir(f"{directory}/data/geometries")
    mkdir(f"{directory}/data/cad")
    shutil.copyfile(f"{os.getcwd()}/flow_params.json", f"{directory}/flow_params.json")
    site_config = {"name": site.name, "magnets": []}
    for site_magnet in site.site_magnets:
        print(
            f"generate_site_config({site_id}): site_magnet={site_magnet.magnet.name}, site_magnet={site_magnet.active}"
        )
        # if not site_magnet.active:
        #     continue
        magnet = site_magnet.magnet
        # print(f'site_magnet: name={magnet.name} id={magnet.id}')
        if magnet.geometry:
            print(f"download: magnet geometry={magnet.geometry.filename}")
            magnet.geometry.download(
                f"{directory}/data/geometries/{magnet.geometry.filename}"
            )
        for magnet_part in magnet.magnet_parts:
            print(f"magnet_part: name={magnet_part.part.name}")
            # if not magnet_part.active:
            #     continue
            for geometry in magnet_part.part.geometries:
                print(f"download: magnet geometry={geometry.attachment.filename}")
                geometry.attachment.download(
                    f"{directory}/data/geometries/{geometry.attachment.filename}"
                )
            if magnet_part.part.cad:
                for cad in magnet_part.part.cad:
                    cad.attachment.download(
                        f"{directory}/data/cad/{cad.attachment.filename}"
                    )
        with open(f"{directory}/{magnet.name}-data.json", "w+") as file:
            magnet_config = generate_magnet_config(magnet.id)
            file.write(json.dumps(magnet_config))
            site_config["magnets"].append({magnet.name: magnet_config})
        # print(f'generate_site_directory: site_config={site_config}')

    with open(f"{directory}/config.json", "w+") as file:
        file.write(json.dumps(site_config))
        return site_config

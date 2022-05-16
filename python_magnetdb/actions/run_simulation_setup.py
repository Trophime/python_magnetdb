import json
import os
import shutil
import subprocess
import tempfile
from argparse import Namespace
from os.path import basename

from python_magnetsetup.config import appenv
from python_magnetsetup.setup import setup

from python_magnetdb.actions.generate_simulation_config import generate_simulation_config
from python_magnetdb.models.attachment import Attachment
from python_magnetdb.models.magnet import Magnet


def prepare_directory(simulation, directory):
    magnet = Magnet.with_('magnet_parts.part.geometry', 'magnet_parts.part.cad.attachment', 'geometry',
                          'magnet_parts.part.material', 'site_magnets.site', 'cad.attachment').find(simulation.resource_id)
    os.mkdir(f"{directory}/data")
    os.mkdir(f"{directory}/data/geometries")
    os.mkdir(f"{directory}/data/cad")
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
        file.write(json.dumps(generate_simulation_config(simulation)))


def run_simulation_setup(simulation):
    simulation.setup_status = "in_progress"
    simulation.save()

    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = "/home/remi/test"
        subprocess.run([f"rm -rf {tempdir}"], shell=True)
        subprocess.run([f"mkdir -p {tempdir}"], shell=True)

        print(f"generating config in {tempdir}...")
        prepare_directory(simulation, tempdir)
        subprocess.run([f"ls -lR {tempdir}"], shell=True)
        print("generating config done")

        print("running setup...")
        data_dir = f"{tempdir}/data"
        current_dir = os.getcwd()
        os.chdir(tempdir)
        
        args = Namespace(wd=tempdir,
                         datafile=f"{tempdir}/config.json",
                         method=simulation.method,
                         time="static" if simulation.static else "transient",
                         geom=simulation.geometry,
                         model=simulation.model,
                         nonlinear=simulation.non_linear,
                         cooling=simulation.cooling,
                         flow_params=f"{tempdir}/flow_params.json",
                         debug=False,
                         verbose=False,
                         skip_archive=True)

        # todo: envfile=None
        env = appenv(envfile=None, url_api=data_dir, yaml_repo=f"{data_dir}/geometries", cad_repo=f"{data_dir}/cad",
                     mesh_repo=data_dir, simage_repo=data_dir, mrecord_repo=data_dir, optim_repo=data_dir)
        try:
            with open(f"{tempdir}/config.json", "r") as config_file:
                config = json.load(config_file)
                setup(env, args, config, f"{tempdir}/{simulation.resource.name}")
            output_archive = f"{tempdir}/output.tar.gz"
            subprocess.run([f"tar cvzf {output_archive} *"], shell=True)
            attachment = Attachment.raw_upload(basename(output_archive), "application/x-tar", output_archive)
            simulation.setup_output_attachment().associate(attachment)
            simulation.setup_status = "done"
        except Exception as e:
            simulation.setup_status = "failed"
            os.chdir(current_dir)
            simulation.save()
            raise e
        os.chdir(current_dir)
        simulation.save()

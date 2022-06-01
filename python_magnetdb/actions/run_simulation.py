import os
import shlex
import subprocess
import tempfile
from os.path import basename

from python_magnetdb.models.attachment import Attachment


def run_simulation(simulation):
    simulation.status = "in_progress"
    simulation.save()

    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = "/home/remi/test"
        subprocess.check_output([f"rm -rf {tempdir}"], shell=True)
        subprocess.check_output([f"mkdir -p {tempdir}"], shell=True)

        current_dir = os.getcwd()
        os.chdir(tempdir)
        try:
            proc = subprocess.check_output(["whoami"], shell=False)
            print(f"Whoami: {proc}")
            
            print("Downloading setup archive...")
            simulation.setup_output_attachment.download(f"{tempdir}/setup.tar.gz")
            print("Extracting setup archive...")
            exec_cmd = f"tar xvf {tempdir}/setup.tar.gz -C {tempdir}"
            proc = subprocess.check_output(shlex.split(exec_cmd), shell=True)
            print("Finding config file...")
            config_file_path = None
            for file in os.listdir(tempdir):
                if file.endswith('.cfg'):
                    config_file_path = f"{tempdir}/{file}"
                    break
            print("Updating configuration...")
            proc = subprocess.check_output([f"perl -pi -e 's|# mesh.scale =|mesh.scale =|' {config_file_path}"], shell=True, stderr=subprocess.STDOUT)
            proc = subprocess.check_output([f"perl -pi -e 's|mesh.filename=.*|mesh.filename=\$cfgdir/data/geometries/test-Axi_withAir.msh|' {config_file_path}"], shell=True, stderr=subprocess.STDOUT)
            exec_cmd = f"singularity exec -B {tempdir}:{tempdir} /home/singularity/hifimagnet-salome-9.8.0.sif salome -w1 -t $HIFIMAGNET/HIFIMAGNET_Cmd.py args:test.yaml,--axi,--air,2,2,--wd,{tempdir}/data/geometries"
            proc = subprocess.check_output([exec_cmd], shell=True, stderr=subprocess.STDOUT, env={"HIFIMAGNET": "/opt/SALOME-9.8.0-UB20.04/INSTALL/HIFIMAGNET/bin/salome"})
            print("Generating Mesh...")
            exec_cmd = f"singularity exec -B {tempdir}:{tempdir} /home/singularity/hifimagnet-salome-9.8.0.sif python3 -m python_magnetgeo.xao test-Axi_withAir.xao --wd {tempdir}/data/geometries mesh --group CoolingChannels --geo test.yaml --lc=1"
            proc = subprocess.check_output([exec_cmd], shell=True, stderr=subprocess.STDOUT)
            print("Running simulation...")
            exec_cmd = f"singularity exec  -B {tempdir}:{tempdir} /home/singularity/feelpp-toolboxes-v0.110.0-alpha.3.sif mpirun -np 8 feelpp_toolbox_coefficientformpdes --directory {tempdir} --config-file {config_file_path}"
            proc = subprocess.check_output([exec_cmd], shell=True, stderr=subprocess.STDOUT)
            print("Archiving results...")
            output_archive = f"{tempdir}/output.tar.gz"
            proc = subprocess.check_output([f"tar cvzf {output_archive} *"], shell=True)
            attachment = Attachment.raw_upload(basename(output_archive), "application/x-tar", output_archive)
            simulation.output_attachment().associate(attachment)
            print("Done!")
            simulation.status = "done"
        except subprocess.CalledProcessError as e:
            print(f'{e.cmd} stderr: {e.stdout.decode()}')
            simulation.status = "failed"
            raise e
        except Exception as e:
            simulation.status = "failed"
            raise e
        os.chdir(current_dir)
        simulation.save()

import os
import shlex
import subprocess
import tempfile
from os.path import basename

from python_magnetdb.models.attachment import Attachment


def run_simulation(simulation):
    simulation.status = "in_progress"
    simulation.save()

    import platform
    system = platform.system()
    if system != 'Linux':
        print(f'run_simulation on localhost: got {system}, only Linux is supported so far')
        simulation.status = "failed"
        return

    with tempfile.TemporaryDirectory() as tempdir:
        subprocess.check_output([f"rm -rf {tempdir}"], shell=True)
        subprocess.check_output([f"mkdir -p {tempdir}"], shell=True)

        current_dir = os.getcwd()
        os.chdir(tempdir)

        try:
            proc = subprocess.check_output(["pwd"], shell=False)
            print(f'pwd: {proc.decode("utf-8")})')

            proc = subprocess.check_output(["whoami"], shell=False)
            print(f'Whoami: {proc.decode("utf-8")}')

            # check number of process
            proc = subprocess.check_output(shlex.split('/usr/bin/getconf _NPROCESSORS_ONLN'), shell=False)
            print(f'Np_max: {proc.decode("utf-8")}')

            # assumes multithreading is on
            NP = int(int(proc.decode("utf-8"))/2)
            print(f'Np: {NP}')

            setup_archive = f'setup.tar.gz'
            print(f'Downloading setup archive... {setup_archive}')
            simulation.setup_output_attachment.download(setup_archive)
            print("Extracting setup archive...")
            exec_cmd = f'tar -zxvf {setup_archive}'
            proc = subprocess.check_output(shlex.split(exec_cmd), shell=False)

            exec_cmd = f"ls -lrth {tempdir}"
            proc = subprocess.check_output(shlex.split(exec_cmd), shell=False)
            print(f'{tempdir}: {proc.decode("utf-8")})')

            config_file_path = None
            for file in os.listdir(tempdir):
                if file.endswith('.cfg'):
                    config_file_path = f"{tempdir}/{file}"
                    break
            print(f'Finding config file... {config_file_path}')

            # TODO get real yaml file
            # only for HL-test so far
            print("Generating CAD...")
            exec_cmd = f"singularity exec -B $PWD:{tempdir} /home/singularity/hifimagnet-salome-9.8.0.sif salome -w1 -t $HIFIMAGNET/HIFIMAGNET_Cmd.py args:test.yaml,--axi,--air,2,2,--wd,{tempdir}/data/geometries"
            proc = subprocess.check_output([exec_cmd], shell=True, stderr=subprocess.STDOUT, env={"HIFIMAGNET": "/opt/SALOME-9.8.0-UB20.04/INSTALL/HIFIMAGNET/bin/salome"})

            # TODO get real xao file
            # only for Axi so far
            print("Generating Mesh...")
            exec_cmd = f"singularity exec -B $PWD:{tempdir} /home/singularity/hifimagnet-salome-9.8.0.sif python3 -m python_magnetgeo.xao test-Axi_withAir.xao --wd {tempdir}/data/geometries mesh --group CoolingChannels --geo test.yaml --lc=1"
            proc = subprocess.check_output([exec_cmd], shell=True, stderr=subprocess.STDOUT)
            
            # TODO get real mesh file
            print("Updating configuration...")
            proc = subprocess.check_output([f"perl -pi -e 's|# mesh.scale =|mesh.scale =|' {config_file_path}"], shell=True, stderr=subprocess.STDOUT)
            proc = subprocess.check_output([f"perl -pi -e 's|mesh.filename=.*|mesh.filename=\$cfgdir/data/geometries/test-Axi_withAir.msh|' {config_file_path}"], shell=True, stderr=subprocess.STDOUT)

            print("Running simulation...")
            exec_cmd = f"singularity exec  -B $PWD:{tempdir} /home/singularity/feelpp-toolboxes-v0.110.0-alpha.3.sif mpirun -np {NP} feelpp_toolbox_coefficientformpdes --directory {tempdir} --config-file {config_file_path}"
            proc = subprocess.check_output([exec_cmd], shell=True, stderr=subprocess.STDOUT)
            
            with open('res.log', 'w') as output:
                output.write(proc.decode("utf-8"))

            print("Archiving results...")
            simulation_name = os.path.basename(os.path.splitext(config_file_path)[0])
            output_archive = f"{tempdir}/{simulation_name}.tar.gz"
            proc = subprocess.check_output([f"tar cvzf {output_archive} *"], shell=True)
            attachment = Attachment.raw_upload(basename(output_archive), "application/x-tar", output_archive)
            simulation.output_attachment().associate(attachment)
            print("Done!")
            simulation.status = "done"
        except subprocess.CalledProcessError as e:
            print(f'{e.cmd} stderr: {e.stdout.decode()}')
            simulation.status = "failed"
            # raise e
            pass

        except Exception as e:
            simulation.status = "failed"
            # raise e
            pass

        os.chdir(current_dir)
        simulation.save()

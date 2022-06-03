import tempfile

import MagnetTools.Bmap as bmap
import MagnetTools.MagnetTools as mt
import numpy as np
from python_magnetsetup.ana import magnet_setup
from python_magnetsetup.config import appenv

from python_magnetdb.actions.generate_magnet_directory import generate_magnet_directory

plotmethod = {
    'Bz': (bmap.getBz, '[T]', 'Magnetic Field Bz'),
    'Br': (bmap.getBr, '[T]', 'Magnetic Field Bz'),
    'B': (bmap.getB, '[T]', 'Magnetic Field'),
    'A': (bmap.getA, '[A/m]', 'Magnetic Potential'),
}


def get_magnet_data(magnet_id):
    with tempfile.TemporaryDirectory() as tempdir:
        config_data = generate_magnet_directory(magnet_id, tempdir)
        data_dir = f"{tempdir}/data"
        env = appenv(envfile=None, url_api=data_dir, yaml_repo=f"{data_dir}/geometries", cad_repo=f"{data_dir}/cad",
                     mesh_repo=data_dir, simage_repo=data_dir, mrecord_repo=data_dir, optim_repo=data_dir)
        return magnet_setup(env, config_data, True)


def prepare_bmap_chart_params(data, i_h, i_b, i_s, n, r0, z0, r, z, pkey, command):
    (Tubes,Helices,OHelices,BMagnets,UMagnets,Shims) = data
    icurrents = mt.get_currents(Tubes, Helices, BMagnets, UMagnets)

    return (
        i_h if i_h is not None else (icurrents[0] if len(icurrents) > 0 else 0),
        i_b if i_b is not None else (icurrents[1] if len(icurrents) > 1 else 0),
        i_s if i_s is not None else 0,
        n if n is not None else 80,
        r0 if r0 is not None else 0,
        z0 if z0 is not None else 0,
        r if r is not None else (0, 3.14),
        z if z is not None else (-3.14, 3.14),
        pkey if pkey is not None else "Bz",
        command if command is not None else "1D_z",
    )


def compute_bmap_chart(data, i_h, i_b, i_s, n, r0, z0, r, z, pkey, command):
    def update_current():
        (Tubes,Helices,OHelices,BMagnets,UMagnets,Shims) = data

        icurrents = mt.get_currents(Tubes, Helices, BMagnets, UMagnets)
        n_magnets = len(icurrents)
        mcurrents = icurrents
        print("n_magnets", n_magnets)
        print("icurrents", icurrents)
        for j,Tube in enumerate(Tubes):
            print(f"Tube[{j}]", Tube.get_n_elem(), Tube.get_index())
            for i in range(Tube.get_n_elem()):
                print(f"H[{i}]: j={Helices[i + Tube.get_index()].get_CurrentDensity()}")
        Bz0 = mt.MagneticField(Tubes, Helices, BMagnets, UMagnets, 0, 0)[1]
        print("Bz0=", Bz0)

        # update Ih, Ib, Is range
        vcurrents = list(icurrents)
        num = 0
        if len(Tubes) != 0: vcurrents[num] = i_h; num += 1
        if len(BMagnets) != 0: vcurrents[num] = i_b; num += 1
        if len(UMagnets) != 0: vcurrents[num] = i_s; num += 1

        currents = mt.DoubleVector(vcurrents)
        print(f"currents= set to {vcurrents}")
        mt.set_currents(Tubes, Helices, BMagnets, UMagnets, OHelices, currents)
        print("actual currents", mt.get_currents(Tubes, Helices, BMagnets, UMagnets) )
        Bz0 = mt.MagneticField(Tubes, Helices, BMagnets, UMagnets, 0, 0)[1]
        print("Bz0=", Bz0)

    def sine():
        print("panel_bmap: compute b")
        (Tubes,Helices,OHelices,BMagnets,UMagnets,Shims) = data
        if command == '1D_z':
            x = np.linspace(z[0], z[1], n)
            B_ = np.vectorize(plotmethod[pkey][0], excluded=[0, 2, 3, 4, 5])
            Bval = lambda y: B_(r0, x, Tubes, Helices, BMagnets, UMagnets)
            return x, Bval(x)

        if command == '1D_r':
            x = np.linspace(r[0], r[1], n)
            B_ = np.vectorize(plotmethod[pkey][0], excluded=[1, 2, 3, 4, 5])
            Bval = lambda y: B_(x, z0, Tubes, Helices, BMagnets, UMagnets)
            return x, Bval(x)

    def compute_max():
        (Tubes,Helices,OHelices,BMagnets,UMagnets,Shims) = data

        # get current for max
        icurrents = mt.get_currents(Tubes, Helices, BMagnets, UMagnets)
        vcurrents = list(icurrents)
        num = 0
        if len(Tubes) != 0: vcurrents[num] = 31.e+3; num += 1
        if len(BMagnets) != 0: vcurrents[num] = 31.e+3; num += 1
        if len(UMagnets) != 0: vcurrents[num] = 0; num += 1

        Bz0 = mt.MagneticField(Tubes, Helices, BMagnets, UMagnets, 0, 0)[1]

        currents = mt.DoubleVector(vcurrents)
        mt.set_currents(Tubes, Helices, BMagnets, UMagnets, OHelices, currents)
        x, y = sine()
        return y

    update_current()
    x, y = sine()

    return dict(x=x.tolist(), y=y.tolist(), ymax=compute_max().tolist(), yaxis=plotmethod[pkey][1])

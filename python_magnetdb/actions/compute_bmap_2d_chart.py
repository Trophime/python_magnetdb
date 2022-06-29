import MagnetTools.Bmap as bmap
import MagnetTools.MagnetTools as mt
import numpy as np


plotmethod = {
    'Bz': (bmap.getBz, '[T]', 'Magnetic Field Bz', [2, 3, 4, 5]),
    'Br': (bmap.getBr, '[T]', 'Magnetic Field Bz', [2, 3, 4, 5]),
    'B': (bmap.getB, '[T]', 'Magnetic Field', [2, 3, 4, 5]),
    'A': (bmap.getA, '[A/m]', 'Magnetic Potential', [2, 3, 4, 5]),
    'G': (bmap.getGradMagnetoGravPotential, '[%]', 'He Levitation Force Homogeneity', [2, 3, 4, 5, 6]),
}


def prepare_bmap_2d_chart_params(data, i_h, i_b, i_s, nr, r0, r1, nz, z0, z1, pkey):
    (Tubes,Helices,OHelices,BMagnets,UMagnets,Shims) = data
    icurrents = mt.get_currents(Tubes, Helices, BMagnets, UMagnets)

    return (
        i_h if i_h is not None else (icurrents[0] if len(icurrents) > 0 else 0),
        i_b if i_b is not None else (icurrents[1] if len(icurrents) > 1 else 0),
        i_s if i_s is not None else (icurrents[2] if len(icurrents) > 2 else 0),
        nr if nr is not None else 10,
        r0 if r0 is not None else 0,
        r1 if r1 is not None else 0.2,
        nz if nz is not None else 21,
        z0 if z0 is not None else -0.2,
        z1 if z1 is not None else 0.2,
        pkey if pkey is not None else "Bz",
        ["i_h", "i_b", "i_s"][:len(icurrents)],
    )


def compute_bmap_2d_chart(data, i_h, i_b, i_s, nr, r0, r1, nz, z0, z1, pkey):
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

    (Tubes,Helices,OHelices,BMagnets,UMagnets,Shims) = data
    
    update_current()

    y = np.linspace(z0, z1, nz)
    x = np.linspace(r0, r1, nr)
    values = []
    B_ = np.vectorize(plotmethod[pkey][0], excluded=plotmethod[pkey][-1])
    print(f"plot {pkey}")
    if pkey == "G":
        for y_value in y:
            values.append(B_(x, y_value, Tubes, Helices, BMagnets, UMagnets, Shims, G0=-2050).tolist())
    else:
        for y_value in y:
            values.append(B_(x, y_value, Tubes, Helices, BMagnets, UMagnets).tolist())

    return dict(x=x.tolist(), y=y.tolist(), values=values, xaxis={'title':{'text': "r[m]"}}, yaxis={'title':{'text': "z[m]"}}, colorbar={'title': plotmethod[pkey][1]})

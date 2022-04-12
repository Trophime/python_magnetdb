import pandas as pd
import numpy as np

import os
cwd = os.getcwd()

import panel as pn
pn.extension()

import param
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure, curdoc


from python_magnetrun.python_magnetrun import MagnetRun

import MagnetTools.MagnetTools as mt
import MagnetTools.Bmap as bmap


# args = pn.state.session_args
print("bmap: __name__", __name__)
# print("bmap: args=", args)

plotmethod={
    'Bz': (bmap.getBz, '[T]', 'Magnetic Field Bz'),
    'Br': (bmap.getBr, '[T]', 'Magnetic Field Bz'),
    'B': (bmap.getB, '[T]', 'Magnetic Field'),
    'A': (bmap.getA, '[A/m]', 'Magnetic Potential'),
}

class StressPanel(pn.viewable.Viewer):
    ymax = None

    # get Mdata from HL-31.d
    fname = "HL-31.d"    
    single_file = '/data/optims/' + fname
    Mdata = bmap.loadMagnet(single_file)

    (Tubes,Helices,OHelices,BMagnets,UMagnets,Shims) = Mdata

    icurrents = mt.get_currents(Tubes, Helices, BMagnets, UMagnets)
    n_magnets = len(icurrents)
    
    i_h = param.Number(default=icurrents[0], bounds=(0, 35.e+3))
    i_b = param.Number(default=icurrents[1], bounds=(0, 35.e+3))
    i_s = param.Number(default=0, bounds=(0, icurrents[1]))

    # n = param.Integer(default=10, bounds=(10, 1000))
    nr = param.Integer(default=80, bounds=(50, 1000))
    nz = param.Integer(default=80, bounds=(50, 1000))

    r0 = param.Parameter(default=0, doc="r")
    z0 = param.Parameter(default=0, doc="z")
    
    r = param.Range(default=(0, 3.14), bounds=(0, 10), doc="r range")
    z = param.Range(default=(-3.14, 3.14), bounds=(-10, 10), doc="z range")
    
    pkey = param.ObjectSelector(default="Bz", objects=["A", "Br", "Bz", "B"])
    command = param.ObjectSelector(default="1D_z", objects=["1D_r", "1D_z", "2D"])
    
    
    def __init__(self, **params):
        print("panel_stress.__init__ params:", params)
        super().__init__(**params)
    
        self.update_data()  
        self.update_current()

        x, y = self.sine()
        self.ymax = y
        self.cds = ColumnDataSource(data=dict(x=x, y=y, ymax=y))
        self.plot = figure(
            plot_height=400,
            plot_width=400,
            tools="crosshair, pan, reset, save, wheel_zoom",
            sizing_mode="stretch_both",
        )
        
        self.plot.xaxis.axis_label = '[m]' # use symbol + units
        self.plot.yaxis.axis_label = '[T]' # use symbol + units
        
        hover = HoverTool()
        # hover.mode = 'vline'
        
        self.plot.add_tools(hover)
        self.plot.line("x", "y", source=self.cds, line_width=3, line_alpha=0.6)
        self.plot.line("x", "ymax", source=self.cds, line_color='orange', line_width=3, line_alpha=0.6)

    def update_data(self):
        print("panel_stress: update_data")

        # load Mdata
        if pn.state.session_args:
            print("pn.state.session_args:", pn.state.session_args)
        else:
            return

        name = pn.state.session_args['name'][0].decode("utf-8")
        mtype = pn.state.session_args['mtype'][0].decode("utf-8")
        id = pn.state.session_args['id'][0].decode("utf-8")

        from python_magnetsetup.config import appenv
        MyEnv = appenv()
        from python_magnetsetup.ana import setup
        from argparse import Namespace
        args = Namespace(wd="", magnet="",msite="",debug=True,verbose=False)
        
        from sqlmodel import Session, select
        from ..database import engine
        from ..models import Magnet, MSite
        from ..crud import get_magnetid_data, get_msiteid_data 
        if mtype == 'magnet':
            print("Magnet id=", id)
            with Session(engine) as session:
                magnet = session.get(Magnet, id)
                jsonfile = magnet.name
                confdata = get_magnetid_data(session, id)
        else:
            print("Site id=", id)
            with Session(engine) as session:
                msite = session.get(MSite, id)
                jsonfile = msite.name
                mtype = "site"
                confdata = get_msiteid_data(session, id)
                
        with Session(engine) as session:
            self.Mdata = setup(MyEnv, args, confdata, jsonfile, session)
        (Tubes,Helices,OHelices,BMagnets,UMagnets,Shims) = self.Mdata
        print(f"loading mdata from {jsonfile} done")
    
        for j,Tube in enumerate(Tubes):
            print(f"Tube[{j}]", Tube.get_n_elem(), Tube.get_index())
            for i in range(Tube.get_n_elem()):
                print(f"H[{i}]:", Helices[i + Tube.get_index()])

        # Bstacks = mt.VectorOfStacks()
        print("Helices:", len(Tubes))
        print("BMagnets:", len(BMagnets))
        print("UMagnets:", len(UMagnets))
        if len(BMagnets) != 0:
            Bstacks = mt.create_Bstack(BMagnets)
            print("Bstacks:", len(Bstacks))
        if len(UMagnets) != 0:
            Ustacks = mt.create_Ustack(UMagnets)
            print("UStacks:", len(Ustacks))

    @param.depends(
        'nr', 'nz',
        'r', 'z',
        'r0', 'z0',
        'pkey', 
        'command',
        watch=True,
    )
    def compute_max(self):
        print("panel_stress: compute_max")
        (Tubes,Helices,OHelices,BMagnets,UMagnets,Shims) = self.Mdata
        
        # get current for max
        icurrents = mt.get_currents(Tubes, Helices, BMagnets, UMagnets)
        vcurrents = list(icurrents)
        num = 0
        if len(Tubes) != 0: vcurrents[num] = 31.e+3; num += 1
        if len(BMagnets) != 0: vcurrents[num] = 31.e+3; num += 1
        if len(UMagnets) != 0: vcurrents[num] = 0; num += 1
        
        Bz0 = mt.MagneticField(Tubes, Helices, BMagnets, UMagnets, 0, 0)[1]
        print("Bz0=", Bz0)
        
        currents = mt.DoubleVector(vcurrents)
        x, y = self.sine()
        self.ymax = y

    def update_current(self):
        print("panel_stress: update_current")
        (Tubes,Helices,OHelices,BMagnets,UMagnets,Shims) = self.Mdata
        
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
        if len(Tubes) != 0: vcurrents[num] = self.i_h; num += 1
        if len(BMagnets) != 0: vcurrents[num] = self.i_b; num += 1
        if len(UMagnets) != 0: vcurrents[num] = self.i_s; num += 1
        
        currents = mt.DoubleVector(vcurrents)
        print(f"currents= set to {vcurrents}")
        mt.set_currents(Tubes, Helices, BMagnets, UMagnets, OHelices, currents)
        print("actual currents", mt.get_currents(Tubes, Helices, BMagnets, UMagnets) )
        for j,Tube in enumerate(Tubes):
            print(f"Tube[{j}]", Tube.get_n_elem(), Tube.get_index())
            for i in range(Tube.get_n_elem()):
                print(f"H[{i}]: j={Helices[i + Tube.get_index()].get_CurrentDensity()}")

        Bz0 = mt.MagneticField(Tubes, Helices, BMagnets, UMagnets, 0, 0)[1]
        print("Bz0=", Bz0)

    def sine(self):
        print("panel_stress: compute b")
        (Tubes,Helices,OHelices,BMagnets,UMagnets,Shims) = self.Mdata
        if self.command == '1D_z':
            x = np.linspace(self.z[0], self.z[1], self.nz)
            B_ = np.vectorize(plotmethod[self.pkey][0], excluded=[0, 2, 3, 4, 5])
            Bval = lambda y: B_(self.r0, x, Tubes, Helices, BMagnets, UMagnets)
            return x, Bval(x)

        if self.command == '1D_r':
            x = np.linspace(self.r[0], self.r[1], self.nr)
            B_ = np.vectorize(plotmethod[self.pkey][0], excluded=[1, 2, 3, 4, 5])
            Bval = lambda y: B_(x, self.z0, Tubes, Helices, BMagnets, UMagnets)
            return x, Bval(x)

    @param.depends(
        'i_h', 'i_b', 'i_s',
        'nr', 'nz',
        'r', 'z',
        'r0', 'z0',
        'pkey', 
        'command',
        watch=True,
    )
    def update_plot(self):
        self.update_data()
        self.update_current()
        x, y = self.sine()
        self.cds.data = dict(x=x, y=y, ymax=self.ymax)

    def __panel__(self):
        print("panel_stress.__panel__")
        name = "HL-31"
        if 'name' in pn.state.session_args:
            name = pn.state.session_args['name'][0].decode("utf-8")
        return pn.Row(pn.Column(f"## HoopStressMap", f"### site:{name}", self.param), self.plot, sizing_mode="stretch_height")

if __name__ == "__main__":
    print("stressmap: call main")
    app = StressPanel()
    app.show(port=5007)
elif __name__.startswith("bokeh"):
    print("stressp: call bokeh")
    app = StressPanel()
    app.servable()

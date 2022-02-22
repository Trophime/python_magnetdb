from pickletools import read_uint2
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
# , getBr, getBz, getB, getA, loadMagnet

from .panel_mrecord import load

# args = pn.state.session_args
print("bmap: __name__", __name__)
# print("bmap: args=", args)

plotmethod={
    'Bz': (bmap.getBz, '[T]', 'Magnetic Field Bz'),
    'Br': (bmap.getBr, '[T]', 'Magnetic Field Bz'),
    'B': (bmap.getB, '[T]', 'Magnetic Field'),
    'A': (bmap.getA, '[A/m]', 'Magnetic Potential'),
}

class BMapPanel(pn.viewable.Viewer):
    # get Mdata
    fname = "HL-31.d"    
    single_file = '/data/optims/' + fname
    Mdata = bmap.loadMagnet(single_file)

    (Tubes,Helices,OHelices,BMagnets,UMagnets,Shims) = Mdata

    icurrents = mt.get_currents(Tubes, Helices, BMagnets, UMagnets)
    n_magnets = len(icurrents)
    

    i_h = param.Number(default=icurrents[0], bounds=(0, icurrents[0]))
    i_b = param.Number(default=icurrents[1], bounds=(0, icurrents[1]))
    i_s = param.Number(default=0, bounds=(0, icurrents[1]))

    # n = param.Integer(default=10, bounds=(10, 1000))
    nr = param.Integer(default=10, bounds=(10, 1000))
    nz = param.Integer(default=10, bounds=(10, 1000))

    r0 = param.Parameter(default=0, doc="r")
    z0 = param.Parameter(default=0, doc="z")
    
    r = param.Range(default=(0, 3.14), bounds=(0, 10), doc="r range")
    z = param.Range(default=(-3.14, 3.14), bounds=(-10, 10), doc="z range")
    
    pkey = param.ObjectSelector(default="Bz", objects=["A", "Br", "Bz", "B"])
    command = param.ObjectSelector(default="1D_z", objects=["1D_r", "1D_z", "2D"])
    
    
    def __init__(self, **params):
        super().__init__(**params)
        print("params:", params)
        print("pn.state.session_args:", pn.state.session_args)

        # load Mdata
        # Mdata = pn.state.session_args['mdata']
        name = pn.state.session_args['name'][0].decode("utf-8")
        mtype = pn.state.session_args['mtype'][0].decode("utf-8")
        id = pn.state.session_args['id'][0].decode("utf-8")

        (Tubes,Helices,OHelices,BMagnets,UMagnets,Shims) = self.Mdata
        
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
            Mdata = setup(MyEnv, args, confdata, jsonfile, session)

        icurrents = mt.get_currents(Tubes, Helices, BMagnets, UMagnets)
        n_magnets = len(icurrents)
        mcurrents = icurrents
        
        # if len(Tubes) == 0: self.i_h.visible = False
        # if len(BMagnets) == 0: self.i_b.visible = False
        # if len(UMagnets) == 0: self.i_s.visible = False

        num = 0
        vcurrents = list(self.icurrents)
        if len(Tubes) != 0: vcurrents[num] = self.i_h; num += 1
        if len(BMagnets) != 0: vcurrents[num] = self.i_b; num += 1
        # if len(UMagnets) != 0: vcurrents[num] = self.i_s; num += 1

        # update Ih, Ib, Is range
        # if no Bitter disable Ib
        # if no Supra disable Is

        Bz0 = mt.MagneticField(Tubes, Helices, BMagnets, UMagnets, 0, 0)[1]
        print("Bz0=", Bz0)

        # update currents
        # compute B
        
        x, y = self.sine()
        self.cds = ColumnDataSource(data=dict(x=x, y=y))
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
        x, y = self.sine()
        self.cds.data = dict(x=x, y=y)
        
    def sine(self):
        print("command:", self.command)
        print("pkey:", self.pkey)

        (Tubes,Helices,OHelices,BMagnets,UMagnets,Shims) = self.Mdata

        num = 0
        vcurrents = list(self.icurrents)
        if len(self.Mdata[0]) != 0: vcurrents[num] = self.i_h; num += 1
        if len(self.Mdata[3]) != 0: vcurrents[num] = self.i_b; num += 1
        if len(self.Mdata[4]) != 0: vcurrents[num] = self.i_s; num += 1
        currents = mt.DoubleVector(vcurrents)
        mt.set_currents(Tubes, Helices, BMagnets, UMagnets, OHelices, currents)
        print("vcurrents:", vcurrents)

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
        """
        if self.command == '2D':
            r = np.linspace(self.r1, self.r2, self.nr)
            z = np.linspace(self.z1, self.z2, self.nz)
            B_ = np.vectorize(plotmethod[self.pkey][0], excluded=[2, 3, 4, 5])

            (x, y) = np.meshgrid(r, z)
            Bval = lambda x,y: B_(x, y, Tubes, Helices, BMagnets, UMagnets)    
        """
        print("x:", x)
        print("Bval:", Bval)
        return x, Bval

    def __panel__(self):
        name = pn.state.session_args['name'][0].decode("utf-8")
        return pn.Row(pn.Column(f"## BMap", f"### site:{name}", self.param), self.plot, sizing_mode="stretch_height")

if __name__ == "__main__":
    # print("bmap: call main")
    app = BMapPanel()
    app.show(port=5007)
elif __name__.startswith("bokeh"):
    # print("bmap: call bokeh")
    app = BMapPanel()
    app.servable()

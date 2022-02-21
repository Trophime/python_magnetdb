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

args = pn.state.session_args
print("__name__", __name__)
print("args=", args)

def load(site: str, filename: str):
    """
    Load dataset
    """
    
    mrun = MagnetRun.fromtxt(site, filename)
    mrun.MagnetData.cleanupData()

    mrun.MagnetData.addTime()
    mrun.MagnetData.removeData('Date')
    mrun.MagnetData.removeData('Time')

    data = mrun.MagnetData.Data
    return data

class MRecordPanel(pn.viewable.Viewer):
    single_file = '/data/mrecords/M9_2019.09.12---22:20:28.txt'
    site = single_file.split('_')[0]
    data = load(site, single_file)
    
    xvariable  = param.Selector(objects=list(data.columns))
    yvariable  = param.Selector(objects=list(data.columns))
    
    def __init__(self, **params):
        super().__init__(**params)
        x, y = self.sine()
        self.cds = ColumnDataSource(data=dict(x=x, y=y))
        self.plot = figure(
            plot_height=400,
            plot_width=400,
            tools="crosshair, pan, reset, save, wheel_zoom",
            sizing_mode="stretch_both",
        )
        
        self.plot.xaxis.axis_label = 'X'
        self.plot.yaxis.axis_label = 'Y'
        
        hover = HoverTool()
        # hover.mode = 'vline'
        
        self.plot.add_tools(hover)
        self.plot.line("x", "y", source=self.cds, line_width=3, line_alpha=0.6)

    @param.depends(
        'xvariable', 
        'yvariable',
        watch=True,
    )
    def update_plot(self):    
        self.param['xvariable'].objects = list(self.data.columns)
        self.param['yvariable'].objects = list(self.data.columns)
        x, y = self.sine()
        self.cds.data = dict(x=x, y=y)
        
    def sine(self):
        x = self.data[self.xvariable].to_numpy()
        y = self.data[self.yvariable].to_numpy()
        return x, y

    def __panel__(self):
        return pn.Row(pn.Column(f"## {self.single_file} {pn.state.session_args['id']}", self.param), self.plot, sizing_mode="stretch_height")

if __name__ == "__main__":
    print("call main")
    app = MRecordPanel()
    app.show(port=5007)
elif __name__.startswith("bokeh"):
    print("call bokeh")
    app = MRecordPanel()
    app.servable()

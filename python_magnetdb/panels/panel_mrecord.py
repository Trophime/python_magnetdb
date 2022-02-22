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

# args = pn.state.session_args
print("mrecord: __name__", __name__)
# print("mrecord: args=", args)

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
    sname = "None"
    fname = "M9_2019.09.12---22:20:28.txt"    
    single_file = '/data/mrecords/' + fname
    site = single_file.split('_')[0]
    data = load(site, single_file)
    id = 2

    url = f"http://localhost:8000/sites/{id}"
    button = pn.widgets.Button(name=sname, button_type = 'primary')
    # button.js_on_click(args={'target': url}, code='window.open(target.value)')
        
    xvariable  = param.Selector(objects=list(data.columns), default='t')
    yvariable  = param.Selector(objects=list(data.columns), default='Field')
    
    def __init__(self, **params):
        super().__init__(**params)
        print("params:", params)
        print("pn.state.session_args:", pn.state.session_args)
        self.fname = pn.state.session_args['name'][0].decode("utf-8")
        self.sname = pn.state.session_args['site_name'][0].decode("utf-8")
        self.single_file = '/data/mrecords/' + self.fname
        self.site = self.single_file.split('_')[0].replace('/data/mrecords/','')
        self.data = load(self.site, self.single_file)

        #self.button.name = self.sname
        #id = pn.state.session_args['id'][0].decode("utf-8")
        #self.url = f"http://localhost:8000/sites/{id}"

        # can we remove uneeded columns from site info ??
        # eg keep Icoil1 for instance and drop Icoili from i=2 to Nhelices for an insert??
        
        x, y = self.sine()
        self.cds = ColumnDataSource(data=dict(x=x, y=y))
        self.plot = figure(
            plot_height=400,
            plot_width=400,
            tools="crosshair, pan, reset, save, wheel_zoom",
            sizing_mode="stretch_both",
        )
        
        self.plot.xaxis.axis_label = 'X' # use symbol + units
        self.plot.yaxis.axis_label = 'Y' # use symbol + units
        
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
        datefield = self.single_file.split('_')[1].replace('.txt','')
        id = pn.state.session_args['id'][0].decode("utf-8")
        return pn.Row(pn.Column(f"## {self.site}", f"### site:{self.sname}", f"### date:{datefield}", self.param), self.plot, sizing_mode="stretch_height")
        # self.button.js_on_click(args={'target': self.url}, code='window.open(target.value)')
        # return pn.Row(pn.Column(f"## {self.site}", self.button, f"### date:{datefield}", self.param), self.plot, sizing_mode="stretch_height")

if __name__ == "__main__":
    # print("call main")
    app = MRecordPanel()
    app.show(port=5007)
elif __name__.startswith("bokeh"):
    # print("call bokeh")
    app = MRecordPanel()
    app.servable()

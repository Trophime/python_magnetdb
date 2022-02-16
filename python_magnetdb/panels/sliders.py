import numpy as np
import panel as pn
import param
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, curdoc


class SineWave(pn.viewable.Viewer):
    offset = param.Number(default=0.0, bounds=(-5.0, 5.0))
    amplitude = param.Number(default=1.0, bounds=(-5.0, 5.0))
    phase = param.Number(default=0.0, bounds=(0.0, 2 * np.pi))
    frequency = param.Number(default=1.0, bounds=(0.1, 5.1))
    N = param.Integer(default=200, bounds=(0, None))
    x_range = param.Range(default=(0, 4 * np.pi), bounds=(0, 4 * np.pi))
    y_range = param.Range(default=(-2.5, 2.5), bounds=(-10, 10))

    def __init__(self, **params):
        super().__init__(**params)
        x, y = self.sine()
        self.cds = ColumnDataSource(data=dict(x=x, y=y))
        self.plot = figure(
            plot_height=400,
            plot_width=400,
            tools="crosshair, pan, reset, save, wheel_zoom",
            x_range=self.x_range,
            y_range=self.y_range,
            sizing_mode="stretch_both",
        )
        self.plot.line("x", "y", source=self.cds, line_width=3, line_alpha=0.6)

    @param.depends(
        "N",
        "frequency",
        "amplitude",
        "offset",
        "phase",
        "x_range",
        "y_range",
        watch=True,
    )
    def update_plot(self):
        x, y = self.sine()
        self.cds.data = dict(x=x, y=y)
        self.plot.x_range.start, self.plot.x_range.end = self.x_range
        self.plot.y_range.start, self.plot.y_range.end = self.y_range

    def sine(self):
        x = np.linspace(0, 4 * np.pi, self.N)
        y = self.amplitude * np.sin(self.frequency * x + self.phase) + self.offset
        return x, y

    def __panel__(self):
        return pn.Row(self.param, self.plot, sizing_mode="stretch_height")

args = pn.state.session_args
print("__name__", __name__)
print("pn args=", args)
if curdoc().session_context:
    args = curdoc().session_context.request.arguments
    print("curdoc args=", args)

if __name__ == "__main__":
    app = SineWave()
    app.show(port=5007)
elif __name__.startswith("bokeh"):
    app = SineWave()
    app.servable()

import param
import panel as pn

pn.extension()

class Example1(param.Parameterized):
    variable  = param.Selector(objects=list('abcdef'), precedence=1)
    window    = param.Integer(default=10, bounds=(1, 20), precedence=1)
    sigma     = param.Number(default=10, bounds=(0, 20), precedence=1)
    hide_button    = param.Boolean(bounds=(0, 1), default=False)
    
    @param.depends('hide_button', watch=True)
    def _hide_them(self):
        precedence = -1 if self.hide_button else 1
        for p_name in ['variable', 'window', 'sigma']:
            self.param[p_name].precedence = precedence

ex1 = RoomOccupancy()

# Display this in a notebok
pn.panel(ex1)

class Example2(param.Parameterized):
    variable  = param.Selector(objects=list('abcdef'))
    window    = param.Integer(default=10, bounds=(1, 20))
    sigma     = param.Number(default=10, bounds=(0, 20))
    hide_button    = param.Boolean(bounds=(0, 1), default=False)
    
    def __init__(self, **params):
        super().__init__(**params)
        self.view = pn.Param(self.param)
    
    @param.depends('hide_button', watch=True)
    def _hide_them(self):
        visible = not self.hide_button
        for p_name in ['variable', 'window', 'sigma']:
            self.view._widgets[p_name].visible = visible

ex2 = Example2()

# Display this in a notebok
ex2.view

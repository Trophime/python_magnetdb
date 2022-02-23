#!/usr/bin/env python
# coding: utf-8

# # Magnet Main Characteristic
# 
# This application allow to load or upload a Magnet description file
# to view:
#     
#     * the generated Magnetic Field profil on Oz axis in "B Profile" tab,
#     * the estimated stress level for Helices in "Hoop Stress"
#     
# To view the field profile or the Hoop stress distribution, 
# you have to click on "apply" button.
# 
# Then you can interactively change the input currents.
# 
# The plot parameters (r and z range) may be changed in "Settings" tab.
# The maximun allowed currents may also be changed in the "Setting" tab.
# **Do not forget** to click on "apply" button to apply your changes.
# 
# NB: When displaying the Hoop stress distribution, **self**
# corresponds to the Hoop stress arising from the self field
# 

# In[ ]:


import ipywidgets as widgets
from ipywidgets import HBox, VBox, HTML
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


#define layout
Ih_slider = widgets.FloatSlider(
    value=0, #icurrents[0],
    min=0,
    max=31.e+3, #icurrents[0],
    description='Ih [A]:',
    readout_format='.1f',
    )
#Ih_slider
Ih_textbox = widgets.FloatText(
        value=31.e+3, #icurrents[0],
        description='Max. Ih [A]:',
        style={'description_width': 'initial'}
    )
dl = widgets.dlink((Ih_textbox, 'value'), (Ih_slider, 'max'))

#Ib_slider: Ib_slider.max = icurrents[1]    
Ib_slider = widgets.FloatSlider(
        value=0, #icurrents[1],
        min=0,
        max=31.e+3, # icurrents[1],
        description='IBitter [A]:',
        readout_format='.1f',
)
Ib_textbox = widgets.FloatText(
        value=31.e+3, #icurrents[1],
        description='Max. IBitter [A]:',
        style={'description_width': 'initial'}
)
dl = widgets.dlink((Ib_textbox, 'value'), (Ib_slider, 'max'))

#Is_slider    
Is_slider = widgets.FloatSlider(
        value=0, #icurrents[2],
        min=0,
        max=0, #icurrents[2],
        description='Isupra [A]:',
        readout_format='.1f',
)
Is_textbox = widgets.FloatText(
        value=0, #icurrents[2],
        description='Max. Isupra [A]:',
        style={'description_width': 'initial'}
)
dl = widgets.dlink((Is_textbox, 'value'), (Is_slider, 'max'))

Mdetails = widgets.HTML(value="<b>Configuration:</b>")
#display(Mdetails)

# TODO:
# add a choice for Bz, Br, B,
# add a choice for r/z plots (2D plots?? not interactive since too long)

# R range slider
r_textbox = widgets.FloatText(
    value=0,
    description='r [m]:',
)

r0_textbox = widgets.FloatText(
    value=0,
    description='r0 [m]:',
)

r1_textbox = widgets.FloatText(
    value=+5,
    description='r1 [m]:',
)

rrange_slider = widgets.FloatRangeSlider(
    value=[0, +2.],
    min=0, max=+5., step=0.1,
    description='r:',
    readout_format='.1f',
)

dl = widgets.dlink((r0_textbox, 'value'), (rrange_slider, 'min'))
dl = widgets.dlink((r1_textbox, 'value'), (rrange_slider, 'max'))
rrange = HBox([r0_textbox, rrange_slider, r1_textbox])

# Z range slider
z_textbox = widgets.FloatText(
    value=0,
    description='z [m]:',
)

z0_textbox = widgets.FloatText(
    value=-5,
    description='z0:',
)

z1_textbox = widgets.FloatText(
    value=+5,
    description='z1:',
)

zrange_slider = widgets.FloatRangeSlider(
    value=[-2., +2.],
    min=-5., max=+5., step=0.1,
    description='z:',
    readout_format='.1f',
)

dl = widgets.dlink((z0_textbox, 'value'), (zrange_slider, 'min'))
dl = widgets.dlink((z1_textbox, 'value'), (zrange_slider, 'max'))
zrange = HBox([z0_textbox, zrange_slider, z1_textbox])


# npts: number of points per plot
npts_textbox = widgets.IntText(
    value=100,
    description='N:',
)

Profil_legend = widgets.HTML(value="<b>Plot range options</b>")
Profil_params = VBox([npts_textbox, rrange, zrange, r_textbox, z_textbox])
Current_legend = widgets.HTML(value="<b>Max. currents values</b>")
Current_params = VBox([Ih_textbox, Ib_textbox, Is_textbox])
Params = VBox([Profil_legend, Profil_params, Current_legend, Current_params])

Bz0_textbox = widgets.FloatText(
    value=0,
    description='Bz(0,0):',
    style={'description_width': 'initial'},
    disabled=True
)

# Field to plot
Fields= widgets.Dropdown(
    options=['Br', 'Bz', 'B'],
    value='Bz',
    description='Field:',
    disabled=False,
)

Axis = widgets.RadioButtons(
    options=['Or', 'Oz'],
    value='Oz',
    description='Select Axis:',
    disabled=False
)

out = widgets.Output()
outfield = widgets.Output()
outbar = widgets.Output()


# In[ ]:


import MagnetTools.MagnetTools as mt
import MagnetTools.Bmap as bmap

from python_magnetsetup.config import appenv
MyEnv = appenv()
        
Bval = None
Mdata = None
icurrents = None
Hoop_ = None

@out.capture()
def Bprofile(args):
    with out:
        print("call loadMagnet %s" % args.magnet)
    
    global Mdata
    try:
        from python_magnetsetup.objects import load_object_from_db
        from python_magnetsetup.ana import setup
        
        MyEnv = appenv()
        if args.magnet:
            confdata = load_object_from_db(MyEnv, "magnet", args.magnet, args.debug)
            jsonfile = args.magnet
        if args.msite:
            confdata = load_object_from_db(MyEnv, "msite", args.msite, args.debug)
            jsonfile = args.msite
            
        Mdata = setup(MyEnv, args, confdata, jsonfile, True) 
    except:
        with out:
            print("Failed to load %s"  % args.magnet)
            
    print("Mdata:", Mdata)
    (Tubes,Helices,OHelices,BMagnets,UMagnets,Shims) = Mdata

    global Bval, Bmax, icurrents, mcurrents, Hoop_headers, Hoop_, Hoopmax_
    
    with out:
        print("call Bprofile")
    icurrents = mt.get_currents(Tubes, Helices, BMagnets, UMagnets)
    n_magnets = len(icurrents)
    mcurrents = icurrents
    
    Bz0 = mt.MagneticField(Tubes, Helices, BMagnets, UMagnets, 0, 0)[1]
    
    # update Currents slider values
    num = 0
    msg = ""
    imsg = ""
    if len(Tubes) != 0:
        Ih_slider.value = icurrents[num]
        Ih_slider.max = icurrents[num]
        msg += "<li>Helices: %d</li>" % len(Tubes)
        imsg += "<li>Helices: %g A</li>" % icurrents[num]
        num += 1
    if len(BMagnets) != 0:
        Ib_slider.value = icurrents[num]
        Ib_slider.max = icurrents[num]
        Bstacks = mt.create_Bstack(BMagnets)
        msg += "<li>Bitters: %d</li>" % len(Bstacks)
        imsg += "<li>Bitters: %g A</</li>" % icurrents[num]
        num += 1
    if len(UMagnets) != 0:
        Is_slider.value=icurrents[num]
        Is_slider.max = icurrents[num]
        Ustacks = mt.create_Ustack(UMagnets)
        msg += "<li>Supras: %d</li>" % len(Ustacks)
        imsg += "<li>Supras: %g A</li>" % icurrents[num]
        num += 1

    details = "<b>Configuration:</b><ul>%s</ul>" % msg
    details += "<b>Nominal Currents:</b><ul>%s</ul>" % imsg
    details += "<b>Nominal Bz(0):</b><ul>%g T</ul>" % Bz0
    Mdetails.value = details
                         
    # how to hide zrange_slider.on_displayed=False
    global Bz0_textbox
    
    Bz0_textbox.value = mt.MagneticField(Tubes, Helices, BMagnets, UMagnets, 0, 0)[1]
    with out:
        print("Bz(0)=", Bz0_textbox.value)
        print("size:", len(Tubes), len(BMagnets), len(UMagnets))
        print("Is_slider:", Is_slider)

    if len(Tubes) == 0:
        Ih_slider.layout.visibility = "hidden"
    else:
        Ih_slider.layout.visibility = "visible"
    if len(BMagnets) == 0:
        Ib_slider.layout.visibility = "hidden"
    else:
        Ib_slider.layout.visibility = "visible"
    if len(UMagnets) == 0:
        Is_slider.layout.visibility = "hidden"
    else:
        Is_slider.layout.visibility = "visible"
    
#    # Get Bmax first
#    if Axis.value == 'Oz':
#        Bz_z = np.vectorize(bmap.plotmethod[Fields.value][0], excluded=[0, 2, 3, 4, 5])
#        Bval = lambda y: Bz_z(r_textbox.value, y, Tubes, Helices, BMagnets, UMagnets)
#    if Axis.value == 'Or':
#        Bz_z = np.vectorize(bmap.plotmethod[Fields.value][0], excluded=[1, 2, 3, 4, 5])
#        Bval = lambda y: Bz_z(z_textbox.value, y, Tubes, Helices, BMagnets, UMagnets)
    
    # Hoop stress max
    (Hoop_headers, Hoop_) = bmap.getHoop(Tubes, Tubes, Helices, BMagnets, UMagnets, "H")
    Hoopmax_ = Hoop_


# In[ ]:


# def plot(xlim, npts, Ih, Ib):
def plot(Ih, Ib, Is):

    global xval, Bval, Bmax, Mdata, icurrents, mcurrents
    
    # shall update title depending on key (ie key='Bz' vs z - now)
    # print("create plot Bz")
    (ax, plt) = bmap.create_plot("[m]", "[T]", title="Magnetic Profile")

    with out:
        print("Field:", Fields.value)
        print("Axis:", Axis.value)
    
    if Bval:
        # print("really plot Bz")
        (Tubes,Helices,OHelices,BMagnets,UMagnets,Shims) = Mdata
        
        # plot range
        r0 = rrange_slider.value[0]
        r1 = rrange_slider.value[1]

        z0 = zrange_slider.value[0]
        z1 = zrange_slider.value[1]
        n = npts_textbox.value

        r = np.linspace(r0, r1, n)
        z = np.linspace(z0, z1, n)

        # get Bmax
        ncurrents = mt.DoubleVector(mcurrents)
        mt.set_currents(Tubes, Helices, BMagnets, UMagnets, OHelices, ncurrents)
        if Axis.value == 'Oz':
            xval = z
            plt.xlabel('Z[m]')
            plt.title('Magnetic Profile (r=%g m)' % r_textbox.value)
        if Axis.value == 'Or' :
            xval = r
            plt.xlabel('r[m]')
            plt.title('Magnetic Profile (z=%g m)' % z_textbox.value)
        lines = bmap.plot1D(xval, Bval, label='nominal', lw=2, color="blue", alpha=0.3, ax=ax)
            
        # update currents
        vcurrents = list(icurrents)
        
        num = 0
        if len(Tubes):
            vcurrents[num] = Ih
            num += 1
        if len(BMagnets):
            vcurrents[num] = Ib
            num += 1
        if len(UMagnets):
            vcurrents[num] = Is
            num += 1
        currents = mt.DoubleVector(vcurrents)
        mt.set_currents(Tubes, Helices, BMagnets, UMagnets, OHelices, currents)

        # check state of textbox, display if not available, update otherwise
        Bz0_textbox.value = mt.MagneticField(Tubes, Helices, BMagnets, UMagnets, 0, 0)[1]

        # lines = ax.plot(z, Bval(z), lw=2, color="red")
        lines = bmap.plot1D(xval, Bval, label='current', lw=2, color="blue", alpha=1, ax=ax)
        
        ax.legend()
            
    plt.show()

# def plot(xlim, npts, Ih, Ib):
def barplot(Ih, Ib, Is):

    global Hoop_headers, Hoop_, Hoop_max, Mdata, icurrents
    
    # print("plot Hoop")
    (ax, plt) = bmap.create_plot("", "[MPa]", title="Hoop Stress")

    if Hoop_:
        with out:
            print("really plot Hoop")
        (Tubes,Helices,OHelices,BMagnets,UMagnets,Shims) = Mdata
        
        # get Bmax
        bmap.plot_Hoop(Hoop_headers, Hoopmax_, label={'Hoop[MPa]': 'nom. Hoop','Self': 'nom/ Self'}, alpha=0.3, ax=ax)
    
        # update currents
        vcurrents = list(icurrents)
        num = 0
        if len(Tubes):
            vcurrents[num] = Ih
            num += 1
        if len(BMagnets):
            vcurrents[num] = Ib
            num += 1
        if len(UMagnets):
            vcurrents[num] = Is
            num += 1

        currents = mt.DoubleVector(vcurrents)
        mt.set_currents(Tubes, Helices, BMagnets, UMagnets, OHelices, currents)

        # check state of textbox, display if not available, update otherwise
        Bz0_textbox.value = mt.MagneticField(Tubes, Helices, BMagnets, UMagnets, 0, 0)[1]

        # lines = ax.plot(z, Bval(z), lw=2, color="red")
        (Hoop_headers, Hoop_) = bmap.getHoop(Tubes, Tubes, Helices, BMagnets, UMagnets, "H")
        bmap.plot_Hoop(Hoop_headers, Hoop_, label={}, alpha=1, ax=ax)
        
        ax.set_xlabel("Helices")
        ax.set_ylabel("[MPa]")
        
        ax.legend()
            
    plt.show()
    
from ipywidgets import interactive
interactive_plot = interactive(plot, Ih=Ih_slider, Ib=Ib_slider, Is=Is_slider)
output = interactive_plot.children[-1]
#output.layout.height = '350px'
#interactive_plot

button_field = widgets.HTML(value="")

interactive_barplot = interactive(barplot, Ih=Ih_slider, Ib=Ib_slider, Is=Is_slider)
output = interactive_barplot.children[-1]
#output.layout.height = '350px'
#interactive_barplot

button_bar = widgets.HTML(value="")

abutton = widgets.Button(
        description='Apply',
)

sbutton = widgets.Button(
    description='Display',
)

buttons = HBox(children=[abutton, sbutton])

# Magnetic Field Profiles
tab1 = VBox(children=[Bz0_textbox, Fields, Axis, interactive_plot, buttons, outfield, button_field])
tab2 = VBox(children=[Bz0_textbox, interactive_barplot, buttons, outbar, button_bar])
tab3 = VBox(children=[Mdetails])
tab4 = VBox(children=[Params])
tab5 = VBox(children=[out])
# tab6 = VBox(children=[output_tab])
    
tab = widgets.Tab(children=[tab1, tab2, tab3, tab4, tab5])
tab.set_title(0, 'B Profile')
tab.set_title(1, 'Hoop Stress')
tab.set_title(2, 'Configuration')
tab.set_title(3, 'Settings')
tab.set_title(4, "Logs")
# tab.set_title(5, "Display")

def downloadfile(comment, filename):
    """
    create a download button for csv file
    """
    
    # create a link to download file
    import base64

    #FILE
    b64 = base64.b64encode(comment.encode())
    payload = b64.decode()

    #BUTTONS
    html_buttons = '''<html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
    <a download="{filename}" href="data:text/csv;base64,{payload}" download>
    <button class="p-Widget jupyter-widgets jupyter-button widget-button mod-warning">Download File</button>
    </a>
    </body>
    </html>
    '''

    return html_buttons.format(payload=payload,filename=filename)

@abutton.on_click
def plot_on_click(b):

    global Mdata, Bval

    with out:
        print("click on button apply")
    if tab.selected_index == 0: 
        
        (Tubes,Helices,OHelices,BMagnets,UMagnets,Shims) = Mdata
        
        # Get Bmax first
        if Axis.value == 'Oz':
            with out:
                print("r_textbox.value=%g" % r_textbox.value)
            
            Bz_z = np.vectorize(bmap.plotmethod[Fields.value][0], excluded=[0, 2, 3, 4, 5])
            Bval = lambda y: Bz_z(r_textbox.value, y, Tubes, Helices, BMagnets, UMagnets)

        if Axis.value == 'Or':
            with out:
                print("z_textbox.value=%g" % z_textbox.value)
            
            Bz_z = np.vectorize(bmap.plotmethod[Fields.value][0], excluded=[1, 2, 3, 4, 5])
            Bval = lambda y: Bz_z(y, z_textbox.value, Tubes, Helices, BMagnets, UMagnets)

        interactive_plot.update()
    if tab.selected_index == 1: 
        interactive_barplot.update()
    # plot(Ih, Ib)

@outfield.capture()
def display_field(xval, Bval, tablefmt, datafile):
    outfield.clear_output(wait=True)

    B_headers = []
    if Axis.value == 'Oz':
        B_headers.append('z[m]')
    if Axis.value == 'Or':
        B_headers.append('r[m]')
    B_headers.append(Fields.value)
    # print("type(xval):",  type(xval))
    # print("type(Bval):",  type(Bval))
    B_ = [ [x,Bval(x)] for x in xval ]
        
    bmap.display_table(B_headers, B_, tablefmt=tablefmt, datafile=datafile)

@outbar.capture()
def display_bar(headers, data_, tablefmt, datafile):
    outbar.clear_output(wait=True)
    bmap.display_table(headers, data_, tablefmt=tablefmt, datafile=datafile)

@sbutton.on_click
def save_on_click(b):
    with out:
        print("click on button display")
    if tab.selected_index == 0: 
        global xval, Bval
        with out:
            print("save Magnetic field profile")
        
        datafile = "tmp/BField.csv"        
        display_field(xval, Bval, tablefmt="simple", datafile=datafile)
        button_field.value = downloadfile('Magnetic Field Distribution', datafile)
        
    if tab.selected_index == 1: 
        global Hoop_headers, Hoop_
        with out:
            print("display Hoop stress")
        
        datafile = "tmp/Hoop.csv"
        display_bar(Hoop_headers, Hoop_, tablefmt="simple", datafile=datafile)
        button_bar.value = downloadfile('Hoop Stress Distribution', datafile)
        
def what_Axis(value):
    
    # out.clear_output()
    with out:
        print(f"{value.keys()} this is the output of all the keys")
        print("-------------")
        print(f"{value.values()} this is the output of all the values")
        print("-------------")
Axis.observe(what_Axis, names = 'value')


# In[ ]:



from python_magnetsetup.objects import list_mtype_db
magnets_list = list_mtype_db(MyEnv, "magnet", True)
msites_list = list_mtype_db(MyEnv, "msite", True)

from ipywidgets import interact, Dropdown
tkey = { "Magnet": magnets_list, "MSite": msites_list}
mtypeW = Dropdown(options = tkey.keys())
objW = Dropdown()

def update_objW_options(*args): # *args represent zero (case here) or more arguments.
    objW.options = tkey[mtypeW.value]
    print("update:", mtypeW.value, objW.options)
objW.observe(update_objW_options) # Here is the trick, i.e. update cityW.options based on countryW.value.
    
@interact(mtype = mtypeW, obj = objW)
def print_obj(mtype, obj):
    objW.options = tkey[mtype]
    print("mtype:", mtype)
    print("obj:", obj, type(obj))
    
    from argparse import Namespace
    args = Namespace(wd="", magnet="",msite="",debug=True,verbose=False)
    if mtype == "Magnet":
        args.magnet = obj
    if mtype == "Msite":
        args.msite = obj

    args.wd = MyEnv.yaml_repo
    print("args.wd=", args.wd)
    Bprofile(args)


# In[ ]:


display(tab)


# In[ ]:





# In[ ]:





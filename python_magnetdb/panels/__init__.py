from .button_click import ButtonClick
from .sliders import SineWave
from .panel_mrecord import MRecordPanel

# Fill out with new models
_models = [
    #  [url, title, model]
    ["buttonclick", "Button Click", ButtonClick],
    ["sinewave", "Sine Wave", SineWave],
    ["mrecordpanel", "MRecord Panel", MRecordPanel]
]

titles = {m[0]: m[1] for m in _models}
serving = {f"/panel/{m[0]}": m[2] for m in _models}

print("serving:", serving)

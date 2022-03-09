from .panel_mrecord import MRecordPanel
from .panel_bmap import BMapPanel
from .panel_stress import StressPanel

# Fill out with new models
_models = [
    #  [url, title, model]
    ["mrecordpanel", "MRecord Panel", MRecordPanel],
    ["bmappanel", "Bmap Panel", BMapPanel],
    ["stressmappanel", "Stress Panel", StressPanel]
]

titles = {m[0]: m[1] for m in _models}
serving = {f"/panel/{m[0]}": m[2] for m in _models}

print("serving:", serving)

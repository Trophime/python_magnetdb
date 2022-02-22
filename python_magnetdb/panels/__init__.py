from .panel_mrecord import MRecordPanel
from .panel_bmap import BMapPanel

# Fill out with new models
_models = [
    #  [url, title, model]
    ["mrecordpanel", "MRecord Panel", MRecordPanel],
    ["bmappanel", "Bmap Panel", BMapPanel]
]

titles = {m[0]: m[1] for m in _models}
serving = {f"/panel/{m[0]}": m[2] for m in _models}

print("serving:", serving)

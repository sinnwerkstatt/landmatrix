from mapping.map_model import MapModel
import landmatrix.models
import editor.models

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

class MapStatus(MapModel):
    old_class = editor.models.Status
    new_class = landmatrix.models.Status

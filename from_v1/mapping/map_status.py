from mapping.map_model import MapModel
import landmatrix.models
import old_editor.models

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

class MapStatus(MapModel):
    old_class = old_editor.models.Status
    new_class = landmatrix.models.Status

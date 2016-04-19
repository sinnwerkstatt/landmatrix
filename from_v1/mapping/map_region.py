from mapping.map_model import MapModel
import landmatrix.models
import old_editor.models

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapRegion(MapModel):
    old_class = old_editor.models.Region
    new_class = landmatrix.models.Region

from mapping.map_model import MapModel
import landmatrix.models
import old_editor.models

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapAgriculturalProduce(MapModel):
    old_class = old_editor.models.AgriculturalProduce
    new_class = landmatrix.models.AgriculturalProduce

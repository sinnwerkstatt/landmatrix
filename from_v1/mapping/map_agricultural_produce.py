from mapping.map_model import MapModel
import landmatrix.models
import editor.models

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapAgriculturalProduce(MapModel):
    old_class = editor.models.AgriculturalProduce
    new_class = landmatrix.models.AgriculturalProduce

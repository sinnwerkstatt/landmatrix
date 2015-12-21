from mapping.map_model import MapModel
import landmatrix.models
import editor.models
from mapping.map_agricultural_produce import MapAgriculturalProduce

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapCrop(MapModel):
    old_class = editor.models.Crop
    new_class = landmatrix.models.Crop
    attributes = {
        'agricultural_produce': 'fk_agricultural_produce',
    }
    depends = [ MapAgriculturalProduce ]

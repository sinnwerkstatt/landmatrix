from mapping.map_model import MapModel
from mapping.map_region import MapRegion
import landmatrix.models
import editor.models

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapCountry(MapModel):
    old_class = editor.models.Country
    new_class = landmatrix.models.Country
    attributes = {
        'region': 'fk_region',
    }
    depends = [ MapRegion ]

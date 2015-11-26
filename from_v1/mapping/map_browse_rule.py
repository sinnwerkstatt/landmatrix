from mapping.map_model import MapModel
import landmatrix.models
import editor.models

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class MapBrowseRule(MapModel):
    old_class = editor.models.BrowseRule
    new_class = landmatrix.models.BrowseRule

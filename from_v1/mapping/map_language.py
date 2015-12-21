from mapping.map_model import MapModel
import landmatrix.models
import editor.models

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

class MapLanguage(MapModel):
    old_class = editor.models.Language
    new_class = landmatrix.models.Language

from from_v1.mapping.map_model import MapModel
import landmatrix.models
import old_editor.models


class MapLanguage(MapModel):
    old_class = old_editor.models.Language
    new_class = landmatrix.models.Language

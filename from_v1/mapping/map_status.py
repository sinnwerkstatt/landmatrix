from mapping.map_model import MapModel
import landmatrix.models
import old_editor.models


class MapStatus(MapModel):
    old_class = old_editor.models.Status
    new_class = landmatrix.models.Status

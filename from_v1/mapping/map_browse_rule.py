from from_v1.mapping.map_model import MapModel
import landmatrix.models
import old_editor.models



class MapBrowseRule(MapModel):
    old_class = old_editor.models.BrowseRule
    new_class = landmatrix.models.BrowseRule

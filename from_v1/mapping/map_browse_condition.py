from from_v1.mapping.map_model import MapModel
import landmatrix.models
import old_editor.models
from from_v1.mapping.map_browse_rule import MapBrowseRule



class MapBrowseCondition(MapModel):
    old_class = old_editor.models.BrowseCondition
    new_class = landmatrix.models.BrowseCondition
    depends = [ MapBrowseRule ]

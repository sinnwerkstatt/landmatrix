from mapping.map_model import MapModel
import landmatrix.models
import old_editor.models



class MapRegion(MapModel):
    old_class = old_editor.models.Region
    new_class = landmatrix.models.Region

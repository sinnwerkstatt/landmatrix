from mapping.map_model import MapModel
import landmatrix.models
import old_editor.models



class MapCurrency(MapModel):
    old_class = old_editor.models.Currency
    new_class = landmatrix.models.Currency




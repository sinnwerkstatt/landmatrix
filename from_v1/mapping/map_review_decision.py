from from_v1.mapping.map_model import MapModel
import landmatrix.models
import old_editor.models



class MapReviewDecision(MapModel):
    old_class = old_editor.models.Review_Decision
    new_class = landmatrix.models.ReviewDecision

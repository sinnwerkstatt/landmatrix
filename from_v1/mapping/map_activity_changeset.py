from from_v1.mapping.map_model import MapModel
import landmatrix.models
import old_editor.models


class MapActivityChangeset(MapModel):
    old_class = old_editor.models.A_Changeset
    new_class = landmatrix.models.HistoricalActivity
    depends = []

    attributes = {
        'fk_activity_id': 'id',
        'timestamp': 'history_date',
        'fk_user': 'history_user',
        'comment': 'comment',
    }

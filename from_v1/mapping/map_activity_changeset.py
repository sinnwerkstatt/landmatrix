from from_v1.mapping.map_model import MapModel
import landmatrix.models
import old_editor.models
from from_v1.migrate import V1, V2



def find_attached_activity(activity_id):
    from old_editor.models import Activity as OldActivity
    from landmatrix.models.activity import Activity as NewActivity
    old_activity = OldActivity.objects.using(V1).get(pk=activity_id)
    new_activity = NewActivity.objects.using(V2).\
        filter(activity_identifier=old_activity.activity_identifier).\
        order_by('id').\
        last()
    # print('find_attached_activity', old_activity.activity_identifier, new_activity.id)
    if new_activity:
        return new_activity.id
    else:
        return None


class MapActivityChangeset(MapModel):
    old_class = old_editor.models.A_Changeset
    new_class = landmatrix.models.HistoricalActivity
    depends = []

    attributes = {
        'fk_activity_id': ('public_version', find_attached_activity),
        'timestamp': 'history_date',
        'fk_user': 'history_user',
        'comment': 'comment',
    }

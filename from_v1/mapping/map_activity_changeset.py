from mapping.map_model import MapModel
import landmatrix.models
import old_editor.models
from migrate import V1, V2

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


def find_attached_activity(activity_id):
    from old_editor.models import Activity as OldActivity
    from landmatrix.models.activity import Activity as NewActivity
    old_activity = OldActivity.objects.using(V1).get(pk=activity_id)
    new_activity = NewActivity.objects.using(V2).\
        filter(activity_identifier=old_activity.activity_identifier).\
        order_by('id').\
        last()
    # print('find_attached_activity', old_activity.activity_identifier, new_activity.id)
    return new_activity.id


class MapActivityChangeset(MapModel):
    old_class = old_editor.models.A_Changeset
    new_class = landmatrix.models.HistoricalActivity
    depends = []

    attributes = {
        'fk_activity_id': ('fk_activity_id', find_attached_activity),
        'comment': 'comment',
        'timestamp': 'timestamp',
    }

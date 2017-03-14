from from_v1.mapping.map_model import MapModel
import landmatrix.models
import old_editor.models
from from_v1.migrate import V1, V2


def get_fk_user_created_id(fk_user_created_id):
    from django.contrib.auth.models import User
    try:
        u = User.objects.using(V2).get(fk=fk_user_created_id)
    except:
        return None


def get_fk_user_assigned_id(fk_user_assigned_id):
    from django.contrib.auth.models import User
    try:
        u = User.objects.using(V2).get(fk=fk_user_assigned_id)
    except:
        return None


class MapActivityFeedback(MapModel):
    old_class = old_editor.models.A_Feedback
    new_class = landmatrix.models.ActivityFeedback
    depends = []

    attributes = {
        'fk_activity': 'fk_activity',
        'fk_user_assigned_id': ('fk_user_assigned_id', get_fk_user_assigned_id),
        'fk_user_created_id': ('fk_user_created_id', get_fk_user_created_id),
        'comment': 'comment',
        'timestamp': 'timestamp',
    }

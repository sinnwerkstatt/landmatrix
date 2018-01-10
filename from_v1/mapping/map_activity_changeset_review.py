from from_v1.mapping.map_model import MapModel
import landmatrix.models
import old_editor.models
from from_v1.migrate import V1, V2


def get_historical_activity_id(fk_a_changeset):
    from old_editor.models import A_Changeset
    try:
        cs = A_Changeset.objects.using(V1).get(pk=fk_a_changeset)
        return cs.fk_activity_id
    except A_Changeset.DoesNotExist:
        return None

def get_fk_user(fk_user):
    from django.contrib.auth.models import User
    if fk_user:
        try:
            u = User.objects.using(V2).get(pk=fk_user)
            return fk_user
        except User.DoesNotExist:
            return None
    else:
        return None


class MapActivityChangesetReview(MapModel):
    old_class = old_editor.models.A_Changeset_Review
    new_class = landmatrix.models.ActivityChangeset
    depends = []

    attributes = {
        'fk_a_changeset_id': ('fk_activity_id', get_historical_activity_id),
        'fk_user_id': ('fk_user_id', get_fk_user),
        'timestamp': 'timestamp',
        'fk_review_decision': 'fk_review_decision',
        'comment': 'comment',
    }
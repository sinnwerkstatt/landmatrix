from from_v1.mapping.map_model import MapModel
import landmatrix.models
import old_editor.models
from from_v1.migrate import V1


def get_historical_activity_id(fk_a_changeset):
    from old_editor.models import A_Changeset
    try:
        cs = A_Changeset.objects.using(V1).get(pk=fk_a_changeset)
        return cs.fk_activity_id
    except A_Changeset.DoesNotExist:
        return None


class MapActivityChangesetReview(MapModel):
    old_class = old_editor.models.A_Changeset_Review
    new_class = landmatrix.models.ActivityChangeset
    depends = []

    attributes = {
        'fk_a_changeset_id': ('fk_activity_id', get_historical_activity_id),
        'fk_user': 'fk_user',
        'timestamp': 'timestamp',
        'fk_review_decision': 'fk_review_decision',
        'comment': 'comment',
    }
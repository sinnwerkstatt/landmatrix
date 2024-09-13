from django.utils import timezone

from freezegun import freeze_time

from apps.landmatrix.tests.helpers import AbstractModelTestCase
from apps.landmatrix.models.abstract import VersionStatus, BaseVersion

PETER = 1
JOHANNA = 2
KNUT = 3


class TestBaseVersionMixin(AbstractModelTestCase):
    abstract_model = BaseVersion

    @freeze_time("2024-07-26")
    def test_copy_to_new_draft(self):
        version: BaseVersion = self.derived_model.objects.create(
            status=VersionStatus.ACTIVATED,
            created_at="2024-01-01",
            created_by_id=PETER,
            modified_at="2024-01-02",
            modified_by_id=JOHANNA,
            sent_to_review_at="2024-01-03",
            sent_to_review_by_id=JOHANNA,
            sent_to_activation_at="2024-01-03",
            sent_to_activation_by_id=JOHANNA,
            activated_at="2024-01-03",
            activated_by_id=KNUT,
        )

        version.copy_to_new_draft(KNUT)

        assert version.id is None
        assert version.status == VersionStatus.DRAFT

        assert version.created_at == timezone.now()
        assert version.created_by_id == KNUT
        assert version.modified_at == timezone.now()
        assert version.modified_by_id == KNUT

        assert version.sent_to_review_at is None
        assert version.sent_to_review_by is None
        assert version.sent_to_activation_at is None
        assert version.sent_to_activation_by is None
        assert version.activated_at is None
        assert version.activated_by is None

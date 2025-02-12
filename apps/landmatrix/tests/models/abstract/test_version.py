from freezegun import freeze_time

from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.accounts.models import User, UserRole
from apps.landmatrix.models.abstract import BaseVersion, VersionStatus
from apps.landmatrix.tests.helpers import AbstractModelTestCase

UserModel = get_user_model()


class TestBaseVersionMixin(AbstractModelTestCase):
    abstract_model = BaseVersion

    @freeze_time("2024-07-26")
    def test_copy_to_new_draft(self):
        # cannot import them as fixtures for some reason
        reporter: User = UserModel.objects.create_user(
            username="reporter",
            password="love2report",  # noqa: S106
            role=UserRole.REPORTER,
        )
        editor: User = UserModel.objects.create_user(
            username="editor",
            password="love2edit",  # noqa: S106
            role=UserRole.EDITOR,
        )
        admin: User = UserModel.objects.create_user(
            username="admin",
            password="love2administrate",  # noqa: S106
            role=UserRole.ADMINISTRATOR,
        )

        version: BaseVersion = self.derived_model.objects.create(
            status=VersionStatus.ACTIVATED,
            created_at="2024-01-01T00:00:00Z",
            created_by=reporter,
            modified_at="2024-01-02T00:00:00Z",
            modified_by=editor,
            sent_to_review_at="2024-01-03T00:00:00Z",
            sent_to_review_by=editor,
            sent_to_activation_at="2024-01-03T00:00:00Z",
            sent_to_activation_by=editor,
            activated_at="2024-01-03T00:00:00Z",
            activated_by=admin,
        )

        version.copy_to_new_draft(admin.id)

        assert version.id is None
        assert version.status == VersionStatus.DRAFT

        assert version.created_at == timezone.now()
        assert version.created_by == admin
        assert version.modified_at == timezone.now()
        assert version.modified_by == admin

        assert version.sent_to_review_at is None
        assert version.sent_to_review_by is None
        assert version.sent_to_activation_at is None
        assert version.sent_to_activation_by is None
        assert version.activated_at is None
        assert version.activated_by is None

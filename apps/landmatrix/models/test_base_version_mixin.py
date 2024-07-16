from .new import BaseVersionMixin


# I did not manage to set up database creation for this test model,
# so I create an in memory object and test its methods/attributes.
class ConcreteVersion(BaseVersionMixin):
    class Meta:
        # needs to be different from landmatrix
        app_label = "test_landmatrix"


def test_copy_to_new_draft():
    version = ConcreteVersion(
        id=500,
        status="IN_REVIEW",
        created_at="2024-01-01",
        created_by_id=1,
        modified_at="2024-01-02",
        modified_by_id=2,
        sent_to_review_at="2024-01-03",
        sent_to_review_by_id=3,
        sent_to_activation_at="2024-01-03",
        sent_to_activation_by_id=4,
        activated_at="2024-01-03",
        activated_by_id=5,
    )

    version.copy_to_new_draft(34)

    assert version.id is None
    assert version.status == "DRAFT"
    # assert version.created_at == timezone.now()
    assert version.created_by_id == 34
    assert version.modified_at is None
    assert version.modified_by is None
    assert version.sent_to_review_at is None
    assert version.sent_to_review_by is None
    assert version.sent_to_activation_at is None
    assert version.sent_to_activation_by is None
    assert version.activated_at is None
    assert version.activated_by is None

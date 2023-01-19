import pytest

from django.contrib.auth import get_user_model

from apps.landmatrix.management.commands.fix_deal_json_fields import (
    forward_deal,
    JSON_fields,
    forward_version,
)

from apps.landmatrix.models.deal import Deal, DealVersion


@pytest.mark.django_db
def test_fix_json_fields_deal():

    d1 = Deal.objects.create(**{field: None for field in JSON_fields})
    d2 = Deal.objects.create(**{field: [] for field in JSON_fields})
    d3 = Deal.objects.create(**{field: [{"current": True}] for field in JSON_fields})

    for deal in [d1, d2, d3]:
        forward_deal(deal)
        deal.save()

    assert all(getattr(d1, field) is None for field in JSON_fields)
    assert all(getattr(d2, field) is None for field in JSON_fields)
    assert all(getattr(d3, field) == [{"current": True}] for field in JSON_fields)


@pytest.mark.django_db()
def test_fix_json_fields_version():

    User = get_user_model()
    user = User.objects.create()
    modifier_fields = {"modified_at": "2000-01-01", "modified_by": user.id}

    v1 = DealVersion.objects.create(
        serialized_data={**{field: None for field in JSON_fields}, **modifier_fields},
    )
    v2 = DealVersion.objects.create(
        serialized_data={**{field: [] for field in JSON_fields}, **modifier_fields},
    )
    v3 = DealVersion.objects.create(
        serialized_data={
            **{field: [{"current": True}] for field in JSON_fields},
            **modifier_fields,
        }
    )

    for version in [v1, v2, v3]:
        forward_version(version)
        version.save()

    assert all(v1.serialized_data[field] is None for field in JSON_fields)
    assert all(v2.serialized_data[field] is None for field in JSON_fields)
    assert all(
        v3.serialized_data[field] == [{"current": True}] for field in JSON_fields
    )

from typing import Type

import pytest

from django.contrib.auth import get_user_model

from apps.accounts.models import User

from ...management.commands.fix_deal_json_fields import (
    JSON_fields,
    forward_deal,
    forward_version,
)
from ...models.deal import DealOld, DealVersionOld

UserModel: Type[User] = get_user_model()

# Todo?! exchange deal old
@pytest.mark.django_db
def test_fix_json_fields_deal():
    d1 = DealOld.objects.create(**{field: None for field in JSON_fields})
    d2 = DealOld.objects.create(**{field: [] for field in JSON_fields})
    d3 = DealOld.objects.create(**{field: [{"current": True}] for field in JSON_fields})

    for deal in [d1, d2, d3]:
        forward_deal(deal)
        deal.save()

    assert all(getattr(d1, field) is None for field in JSON_fields)
    assert all(getattr(d2, field) is None for field in JSON_fields)
    assert all(getattr(d3, field) == [{"current": True}] for field in JSON_fields)


@pytest.mark.django_db()
def test_fix_json_fields_version():
    user = UserModel.objects.create()
    modifier_fields = {"modified_at": "2000-01-01", "modified_by": user.id}

    v1 = DealVersionOld.objects.create(
        serialized_data={**{field: None for field in JSON_fields}, **modifier_fields},
    )
    v2 = DealVersionOld.objects.create(
        serialized_data={**{field: [] for field in JSON_fields}, **modifier_fields},
    )
    v3 = DealVersionOld.objects.create(
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

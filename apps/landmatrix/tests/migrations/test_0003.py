import pytest
from datetime import datetime

JSON_fields = [
    "contract_size",
    "production_size",
    "intention_of_investment",
    "negotiation_status",
    "implementation_status",
    "on_the_lease",
    "off_the_lease",
    "total_jobs_current",
    "foreign_jobs_current",
    "domestic_jobs_current",
    "involved_actors",
    "crops",
    "animals",
    "mineral_resources",
    "contract_farming_crops",
    "contract_farming_animals",
]


@pytest.mark.skip(reason="https://github.com/wagtail/wagtail/issues/1824")
@pytest.mark.django_db()
def test_0003_deal(migrator):
    old_state = migrator.apply_initial_migration(
        ("landmatrix", "0002_auto_20220716_1440")
    )
    Deal = old_state.apps.get_model("landmatrix", "Deal")

    assert Deal.objects.count() == 0

    Deal.objects.create(**{field: None for field in JSON_fields})
    Deal.objects.create(**{field: [] for field in JSON_fields})
    Deal.objects.create(**{field: ["non_empty"] for field in JSON_fields})

    assert Deal.objects.count() == 3

    assert (
        Deal.objects.filter(
            **{f"{field}__isnull": True for field in JSON_fields}
        ).count()
        == 1
    )

    new_state = migrator.apply_tested_migration(
        ("landmatrix", "0003_set_empty_deal_json_fields_to_null")
    )
    Deal = new_state.apps.get_model("landmatrix", "Deal")

    assert Deal.objects.count() == 3

    assert (
        Deal.objects.filter(
            **{f"{field}__isnull": True for field in JSON_fields}
        ).count()
        == 2
    )


@pytest.mark.skip(reason="https://github.com/wagtail/wagtail/issues/1824")
@pytest.mark.django_db()
def test_0003_deal_versions(migrator):
    old_state = migrator.apply_initial_migration(
        ("landmatrix", "0002_auto_20220716_1440")
    )
    DealVersion = old_state.apps.get_model("landmatrix", "DealVersion")

    assert DealVersion.objects.count() == 0

    v1 = DealVersion.objects.create(
        created_at=datetime(2000, 1, 1),
        serialized_data={field: None for field in JSON_fields},
    )
    v2 = DealVersion.objects.create(
        created_at=datetime(2000, 1, 1),
        serialized_data={field: [] for field in JSON_fields},
    )
    v3 = DealVersion.objects.create(
        created_at=datetime(2000, 1, 1),
        serialized_data={field: ["non_empty"] for field in JSON_fields},
    )

    assert DealVersion.objects.count() == 3

    new_state = migrator.apply_tested_migration(
        ("landmatrix", "0003_set_empty_deal_json_fields_to_null")
    )
    DealVersion = new_state.apps.get_model("landmatrix", "DealVersion")

    assert DealVersion.objects.count() == 3

    sdata = DealVersion.objects.get(pk=v1.pk).serialized_data
    assert all(sdata[field] is None for field in JSON_fields)

    sdata = DealVersion.objects.get(pk=v2.pk).serialized_data
    assert all(sdata[field] is None for field in JSON_fields)

    sdata = DealVersion.objects.get(pk=v3.pk).serialized_data
    assert all(sdata[field] is not None for field in JSON_fields)

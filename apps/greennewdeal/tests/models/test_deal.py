import pytest
from reversion.models import Version

from apps.greennewdeal.models import Deal
from apps.landmatrix.models import (
    ActivityAttributeGroup,
    HistoricalActivity,
    HistoricalActivityAttribute,
)


# TODO: erzeuge revision,
#  stelle sicher, dass die location, datasource und dings auch versioniert werden
#  deal: rolle zurueck zu altem deal? brauchen wir das?
#  loesche deal: stelle sicher, dass die revisionen erhalten bleiben?
#    also vermutlich nur als geloescht markieren


# @pytest.fixture
# def create_histivity(django_db_setup):
#     h1 = HistoricalActivity(activity_identifier=1, fk_status_id=2)
#     h1.save(update_elasticsearch=False)


@pytest.mark.django_db
def test_all_status_options():
    ID = 1  # Draft (Pending)
    HistoricalActivity(activity_identifier=ID, fk_status_id=1).save(
        update_elasticsearch=False, trigger_gnd=True
    )
    assert HistoricalActivity.objects.filter(activity_identifier=ID).count() == 1

    deal_draft_only = Deal.objects.get(id=ID)
    assert deal_draft_only.status == deal_draft_only.STATUS_DRAFT
    versions = Version.objects.get_for_object(deal_draft_only)
    assert len(versions) == 1
    assert versions[0].field_dict["id"] == ID
    assert versions[0].field_dict["status"] == deal_draft_only.STATUS_DRAFT

    ID = 2  # Live (Active)
    HistoricalActivity(activity_identifier=ID, fk_status_id=2).save(
        update_elasticsearch=False, trigger_gnd=True
    )
    assert HistoricalActivity.objects.filter(activity_identifier=ID).count() == 1

    deal_live_only = Deal.objects.get(id=ID)
    assert deal_live_only.status == deal_live_only.STATUS_LIVE
    versions = Version.objects.get_for_object(deal_live_only)
    assert len(versions) == 1
    assert versions[0].field_dict["id"] == ID
    assert versions[0].field_dict["status"] == deal_live_only.STATUS_LIVE

    ID = 3  # Live (this time with Overwritten)
    HistoricalActivity(activity_identifier=ID, fk_status_id=3).save(
        update_elasticsearch=False, trigger_gnd=True
    )
    assert HistoricalActivity.objects.filter(activity_identifier=ID).count() == 1

    deal_live_only = Deal.objects.get(id=ID)
    assert deal_live_only.status == deal_live_only.STATUS_LIVE
    versions = Version.objects.get_for_object(deal_live_only)
    assert len(versions) == 1
    assert versions[0].field_dict["id"] == ID
    assert versions[0].field_dict["status"] == deal_live_only.STATUS_LIVE

    # Stati: Deleted, Rejected, To Delete
    for status in [4, 5, 6]:
        HistoricalActivity(activity_identifier=status, fk_status_id=status).save(
            update_elasticsearch=False, trigger_gnd=True
        )
        assert (
            HistoricalActivity.objects.filter(activity_identifier=status).count() == 1
        )

        deal_live_only = Deal.objects.get(id=status)
        assert deal_live_only.status == status
        versions = Version.objects.get_for_object(deal_live_only)
        assert len(versions) == 1
        assert versions[0].field_dict["id"] == status
        assert versions[0].field_dict["status"] == status


@pytest.mark.django_db
def test_updated_activity():
    ID = 5
    # create first draft
    HistoricalActivity(activity_identifier=ID, fk_status_id=1).save(
        update_elasticsearch=False, trigger_gnd=True
    )
    # create live version
    HistoricalActivity(activity_identifier=ID, fk_status_id=2).save(
        update_elasticsearch=False, trigger_gnd=True
    )
    assert HistoricalActivity.objects.filter(activity_identifier=ID).count() == 2

    deal = Deal.objects.get(id=ID)
    assert deal.status == deal.STATUS_LIVE
    versions = Version.objects.get_for_object(deal)
    assert len(versions) == 2
    assert versions[0].field_dict["id"] == ID
    assert versions[0].field_dict["status"] == deal.STATUS_LIVE
    assert versions[1].field_dict["id"] == ID
    assert versions[1].field_dict["status"] == deal.STATUS_DRAFT

    # create another draft
    HistoricalActivity(activity_identifier=ID, fk_status_id=1).save(
        update_elasticsearch=False, trigger_gnd=True
    )
    deal.refresh_from_db()
    assert deal.status == deal.STATUS_LIVE_AND_DRAFT
    versions = Version.objects.get_for_object(deal)
    assert len(versions) == 3
    assert versions[0].field_dict["status"] == deal.STATUS_DRAFT
    assert versions[1].field_dict["status"] == deal.STATUS_LIVE
    assert versions[2].field_dict["status"] == deal.STATUS_DRAFT

    # and set it live again
    HistoricalActivity(activity_identifier=ID, fk_status_id=3).save(
        update_elasticsearch=False, trigger_gnd=True
    )
    assert HistoricalActivity.objects.filter(activity_identifier=ID).count() == 4

    deal.refresh_from_db()
    assert deal.status == deal.STATUS_LIVE
    versions = Version.objects.get_for_object(deal)
    assert len(versions) == 4
    assert versions[0].field_dict["id"] == ID
    assert versions[0].field_dict["status"] == deal.STATUS_LIVE
    assert versions[1].field_dict["id"] == ID
    assert versions[1].field_dict["status"] == deal.STATUS_DRAFT


@pytest.mark.django_db
def test_activity_with_attributes():
    ID = 10  # Draft (Pending)
    histact = HistoricalActivity(activity_identifier=ID, fk_status_id=2)
    histact.save(update_elasticsearch=False)

    fk_group = ActivityAttributeGroup.objects.create(id=2, name="testgroup")

    HistoricalActivityAttribute.objects.create(
        fk_activity=histact, name="target_country", value=288, fk_group=fk_group
    )
    HistoricalActivityAttribute.objects.create(
        fk_activity=histact,
        name="location_description",
        value="Loc1",
        fk_group=fk_group,
    )
    HistoricalActivityAttribute.objects.create(
        fk_activity=histact, name="point_lon", value=10.0123, fk_group=fk_group
    )
    HistoricalActivityAttribute.objects.create(
        fk_activity=histact, name="point_lat", value=5.0123, fk_group=fk_group
    )
    histact.save(update_elasticsearch=False, trigger_gnd=True)

    d1 = Deal.objects.get(id=ID)
    loc1 = d1.locations.get()
    assert loc1.point.coords == (10.0123, 5.0123)
    loc_versions = Version.objects.get_for_object(loc1)
    assert len(loc_versions) == 1

    histact2 = HistoricalActivity(activity_identifier=ID, fk_status_id=3)
    histact2.save(update_elasticsearch=False)
    assert histact.id + 1 == histact2.id

    HistoricalActivityAttribute.objects.create(
        fk_activity=histact2,
        name="location_description",
        value="Loc1.a",
        fk_group=fk_group,
    )
    HistoricalActivityAttribute.objects.create(
        fk_activity=histact2, name="point_lon", value=10.456, fk_group=fk_group
    )
    HistoricalActivityAttribute.objects.create(
        fk_activity=histact2, name="point_lat", value=5.456, fk_group=fk_group
    )
    histact2.save(update_elasticsearch=False, trigger_gnd=True)

    d1.refresh_from_db()
    loc1 = d1.locations.get()
    assert loc1.point.coords == (10.456, 5.456)
    assert loc1.description == "Loc1.a"
    loc_versions = Version.objects.get_for_object(loc1)
    assert len(loc_versions) == 2
    assert loc_versions[0].field_dict["point"].coords == (10.456, 5.456)
    assert loc_versions[1].field_dict["point"].coords == (10.0123, 5.0123)

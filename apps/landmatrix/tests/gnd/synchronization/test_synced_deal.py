import pytest
from reversion.models import Version

from apps.landmatrix.models import Deal
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
    hact = HistoricalActivity(activity_identifier=ID, fk_status_id=1)
    hact.save(update_elasticsearch=False)
    hact.trigger_gnd()
    assert HistoricalActivity.objects.filter(activity_identifier=ID).count() == 1

    deal_draft_only = Deal.objects.get(id=ID)
    assert deal_draft_only.status == deal_draft_only.STATUS_DRAFT
    assert deal_draft_only.draft_status == deal_draft_only.DRAFT_STATUS_DRAFT
    versions = Version.objects.get_for_object(deal_draft_only)
    assert len(versions) == 1
    assert versions[0].field_dict["id"] == ID
    assert versions[0].field_dict["status"] == deal_draft_only.STATUS_DRAFT
    assert versions[0].field_dict["draft_status"] == deal_draft_only.DRAFT_STATUS_DRAFT

    ID = 2  # Live (Active)
    hact = HistoricalActivity(activity_identifier=ID, fk_status_id=2)
    hact.save(update_elasticsearch=False)
    hact.trigger_gnd()
    assert HistoricalActivity.objects.filter(activity_identifier=ID).count() == 1

    deal_live_only = Deal.objects.get(id=ID)
    assert deal_live_only.status == deal_live_only.STATUS_LIVE
    assert not deal_live_only.draft_status
    versions = Version.objects.get_for_object(deal_live_only)
    assert len(versions) == 1
    assert versions[0].field_dict["id"] == ID
    assert versions[0].field_dict["status"] == deal_live_only.STATUS_LIVE
    assert versions[0].field_dict["draft_status"] is None

    ID = 3  # Live (this time with Overwritten)
    hact = HistoricalActivity(activity_identifier=ID, fk_status_id=3)
    hact.save(update_elasticsearch=False)
    hact.trigger_gnd()
    assert HistoricalActivity.objects.filter(activity_identifier=ID).count() == 1

    deal_live_only = Deal.objects.get(id=ID)
    assert deal_live_only.status == deal_live_only.STATUS_LIVE
    versions = Version.objects.get_for_object(deal_live_only)
    assert len(versions) == 1
    assert versions[0].field_dict["id"] == ID
    assert versions[0].field_dict["status"] == deal_live_only.STATUS_LIVE

    # Stati: Deleted, Rejected, To Delete
    for status in [4, 5, 6]:
        hact = HistoricalActivity(activity_identifier=status, fk_status_id=status)
        hact.save(update_elasticsearch=False)
        hact.trigger_gnd()
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
    hact = HistoricalActivity(activity_identifier=ID, fk_status_id=1)
    hact.save(update_elasticsearch=False)
    hact.trigger_gnd()
    # create live version
    hactx = HistoricalActivity(activity_identifier=ID, fk_status_id=2)
    hactx.save(update_elasticsearch=False)
    hactx.trigger_gnd()
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
    hact = HistoricalActivity(activity_identifier=ID, fk_status_id=1)
    hact.save(update_elasticsearch=False)
    hact.trigger_gnd()
    deal.refresh_from_db()
    assert deal.status == deal.STATUS_LIVE
    assert deal.draft_status == deal.DRAFT_STATUS_DRAFT
    versions = Version.objects.get_for_object(deal)
    assert len(versions) == 3
    assert versions[0].field_dict["status"] == deal.STATUS_LIVE
    assert versions[0].field_dict["draft_status"] == deal.DRAFT_STATUS_DRAFT
    assert versions[1].field_dict["status"] == deal.STATUS_LIVE
    assert versions[2].field_dict["status"] == deal.STATUS_DRAFT

    # and set it live again
    hact = HistoricalActivity(
        activity_identifier=ID, fully_updated=True, fk_status_id=3
    )
    hact.save(update_elasticsearch=False)
    hact.trigger_gnd()
    assert HistoricalActivity.objects.filter(activity_identifier=ID).count() == 4

    deal.refresh_from_db()
    assert deal.status == deal.STATUS_UPDATED
    versions = Version.objects.get_for_object(deal)
    assert len(versions) == 4
    assert versions[0].field_dict["id"] == ID
    assert versions[0].field_dict["status"] == deal.STATUS_UPDATED
    assert not versions[0].field_dict["draft_status"]
    assert versions[1].field_dict["id"] == ID
    assert versions[1].field_dict["status"] == deal.STATUS_LIVE
    assert versions[1].field_dict["draft_status"] == deal.DRAFT_STATUS_DRAFT


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
    histact.save(update_elasticsearch=False)
    histact.trigger_gnd()

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
    histact2.save(update_elasticsearch=False)
    histact2.trigger_gnd()

    d1.refresh_from_db()
    loc1 = d1.locations.get()
    assert loc1.point.coords == (10.456, 5.456)
    assert loc1.description == "Loc1.a"
    loc_versions = Version.objects.get_for_object(loc1)
    assert len(loc_versions) == 2
    assert loc_versions[0].field_dict["point"].coords == (10.456, 5.456)
    assert loc_versions[1].field_dict["point"].coords == (10.0123, 5.0123)

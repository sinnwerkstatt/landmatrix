import pytest

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
from apps.landmatrix.models.deal import DealVersion
from apps.landmatrix.models.deal_submodels import LocationVersion


@pytest.mark.django_db
def test_all_status_options():
    # Draft (Pending)
    hact = HistoricalActivity(activity_identifier=1, fk_status_id=1)
    hact.save(update_elasticsearch=False)
    hact.trigger_gnd()
    assert HistoricalActivity.objects.filter(activity_identifier=1).count() == 1

    deal_draft_only = Deal.objects.get(id=1)
    assert deal_draft_only.status == deal_draft_only.STATUS_DRAFT
    assert deal_draft_only.draft_status == deal_draft_only.DRAFT_STATUS_DRAFT
    versions = DealVersion.objects.filter(object_id=1)
    assert len(versions) == 1
    assert versions[0].fields["id"] == 1
    assert versions[0].fields["status"] == deal_draft_only.STATUS_DRAFT
    assert versions[0].fields["draft_status"] == deal_draft_only.DRAFT_STATUS_DRAFT

    # Live (Active)
    hact = HistoricalActivity(activity_identifier=2, fk_status_id=2)
    hact.save(update_elasticsearch=False)
    hact.trigger_gnd()
    assert HistoricalActivity.objects.filter(activity_identifier=2).count() == 1

    deal_live_only = Deal.objects.get(id=2)
    assert deal_live_only.status == deal_live_only.STATUS_LIVE
    assert not deal_live_only.draft_status
    versions = DealVersion.objects.filter(object_id=2)
    assert len(versions) == 1
    assert versions[0].fields["id"] == 2
    assert versions[0].fields["status"] == deal_live_only.STATUS_LIVE
    assert versions[0].fields["draft_status"] is None

    # Live (this time with Overwritten)
    hact = HistoricalActivity(activity_identifier=3, fk_status_id=3)
    hact.save(update_elasticsearch=False)
    hact.trigger_gnd()
    assert HistoricalActivity.objects.filter(activity_identifier=3).count() == 1

    deal_live_only = Deal.objects.get(id=3)
    assert deal_live_only.status == deal_live_only.STATUS_LIVE
    versions = DealVersion.objects.filter(object_id=3)
    assert len(versions) == 1
    assert versions[0].fields["id"] == 3
    assert versions[0].fields["status"] == deal_live_only.STATUS_LIVE

    live_historical_activity = HistoricalActivity.objects.get(activity_identifier=2)
    live_historical_activity.fk_status_id = 4
    live_historical_activity.save(update_elasticsearch=False)
    live_historical_activity.trigger_gnd()

    deal = Deal.objects.get(id=2)
    assert deal.status == deal.STATUS_DELETED
    versions = DealVersion.objects.filter(object_id=2)
    assert len(versions) == 2
    assert versions[0].fields["id"] == 2
    assert versions[0].fields["status"] == 4


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
    versions = DealVersion.objects.filter(object_id=ID)
    assert len(versions) == 2
    assert versions[0].fields["id"] == ID
    assert versions[0].fields["status"] == deal.STATUS_LIVE
    assert versions[0].fields["draft_status"] is None
    assert versions[1].fields["id"] == ID
    assert versions[1].fields["status"] == deal.STATUS_DRAFT
    assert versions[1].fields["draft_status"] == deal.STATUS_DRAFT

    # create another draft
    hact = HistoricalActivity(activity_identifier=ID, fk_status_id=1)
    hact.save(update_elasticsearch=False)
    hact.trigger_gnd()
    deal.refresh_from_db()
    assert deal.status == deal.STATUS_LIVE
    assert deal.draft_status == deal.DRAFT_STATUS_DRAFT
    versions = DealVersion.objects.filter(object_id=ID)
    assert len(versions) == 3
    assert versions[0].fields["status"] == deal.STATUS_LIVE
    assert versions[0].fields["draft_status"] == deal.DRAFT_STATUS_DRAFT
    assert versions[1].fields["status"] == deal.STATUS_LIVE
    assert versions[2].fields["status"] == deal.STATUS_DRAFT

    # and set it live again
    hact = HistoricalActivity(
        activity_identifier=ID, fully_updated=True, fk_status_id=3
    )
    hact.save(update_elasticsearch=False)
    hact.trigger_gnd()
    assert HistoricalActivity.objects.filter(activity_identifier=ID).count() == 4

    deal.refresh_from_db()
    assert deal.status == deal.STATUS_UPDATED
    versions = DealVersion.objects.filter(object_id=ID)
    assert len(versions) == 4
    assert versions[0].fields["id"] == ID
    assert versions[0].fields["status"] == deal.STATUS_UPDATED
    assert not versions[0].fields["draft_status"]
    assert versions[1].fields["id"] == ID
    assert versions[1].fields["status"] == deal.STATUS_LIVE
    assert versions[1].fields["draft_status"] == deal.DRAFT_STATUS_DRAFT

    # and create draft and reject it
    hact = HistoricalActivity(activity_identifier=ID, fk_status_id=1)
    hact.save(update_elasticsearch=False)
    hact.trigger_gnd()
    deal.refresh_from_db()
    versions = DealVersion.objects.filter(object_id=ID)
    assert len(versions) == 5
    assert versions[0].fields["id"] == ID
    assert versions[0].fields["status"] == deal.STATUS_UPDATED
    assert versions[0].fields["draft_status"] == deal.DRAFT_STATUS_DRAFT
    hact = HistoricalActivity(activity_identifier=ID, fk_status_id=5)
    hact.save(update_elasticsearch=False)
    hact.trigger_gnd()
    deal.refresh_from_db()
    versions = DealVersion.objects.filter(object_id=ID)
    assert len(versions) == 6
    assert versions[0].fields["id"] == ID
    assert versions[0].fields["status"] == deal.STATUS_UPDATED
    assert versions[0].fields["draft_status"] == deal.DRAFT_STATUS_REJECTED

    # mark hact as "to delete"
    hact = HistoricalActivity(activity_identifier=ID, fk_status_id=6)
    hact.save(update_elasticsearch=False)
    hact.trigger_gnd()
    deal.refresh_from_db()
    versions = DealVersion.objects.filter(object_id=ID)
    assert len(versions) == 7
    assert deal.status == deal.STATUS_UPDATED
    assert versions[0].fields["id"] == ID
    assert versions[0].fields["status"] == deal.STATUS_UPDATED
    assert versions[0].fields["draft_status"] == deal.DRAFT_STATUS_TO_DELETE

    # and delete it
    hact = HistoricalActivity(activity_identifier=ID, fk_status_id=4)
    hact.save(update_elasticsearch=False)
    hact.trigger_gnd()
    deal.refresh_from_db()
    versions = DealVersion.objects.filter(object_id=ID)
    assert len(versions) == 8
    assert deal.status == deal.STATUS_DELETED
    assert versions[0].fields["id"] == ID
    assert versions[0].fields["status"] == deal.STATUS_DELETED
    assert versions[0].fields["draft_status"] is None


@pytest.mark.django_db
def test_activity_with_attributes():
    ID = 10
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
    loc_versions = LocationVersion.objects.filter(object_id=loc1.id)
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
    loc_versions = LocationVersion.objects.filter(object_id=loc1.id)
    assert len(loc_versions) == 2
    assert loc_versions[0].fields["point"].coords == (10.456, 5.456)
    assert loc_versions[1].fields["point"].coords == (10.0123, 5.0123)


@pytest.mark.django_db
def test_activity_draft_with_location():
    ID = 15
    histact = HistoricalActivity(activity_identifier=ID, fk_status_id=2)
    histact.save(update_elasticsearch=False)
    histact.trigger_gnd()
    d15 = Deal.objects.get(id=15)
    assert d15
    assert not d15.locations.exists()

    fk_group = ActivityAttributeGroup.objects.create(id=5, name="testgroup")

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
    histact.fully_updated = True
    histact.fk_status_id = 1
    histact.save(update_elasticsearch=False)
    histact.trigger_gnd()

    d15.refresh_from_db()
    versions = DealVersion.objects.filter(object_id=d15.id)
    assert len(versions) == 2
    assert versions[0].fields["fully_updated"]
    assert not versions[1].fields["fully_updated"]
    assert not d15.fully_updated
    assert not d15.locations.exists()

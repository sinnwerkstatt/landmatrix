import pytest
from django.utils import timezone
from reversion.models import Version

from apps.landmatrix.models import Investor
from apps.landmatrix.models import HistoricalInvestor

NAME = "The Grand Investor"
COMMENT = "regular blabla comment"
HOMEPAGE = "https://grandinvestor.the"
OPENCORP = "http://closed.com"
ACTION_COMM = "AKTION!"


@pytest.fixture
def histvestor_draft(db) -> HistoricalInvestor:
    now = timezone.now()
    histvestor = HistoricalInvestor(
        investor_identifier=1,
        fk_status_id=Investor.STATUS_DRAFT,
        name=NAME,
        classification=10,
        history_date=now,
        fk_country_id=604,
        comment=COMMENT,
        action_comment=ACTION_COMM,
        homepage=HOMEPAGE,
        opencorporates_link=OPENCORP,
    )
    histvestor.save(update_elasticsearch=False, trigger_gnd=True)
    assert HistoricalInvestor.objects.filter(investor_identifier=1).count() == 1
    return histvestor


@pytest.fixture
def histvestor_draft_live(histvestor_draft) -> HistoricalInvestor:
    histvestor_draft.fk_status_id = 2
    histvestor_draft.action_comment = "Approved"
    histvestor_draft.save(update_elasticsearch=False, trigger_gnd=True)
    return histvestor_draft


def test_new_investor_draft(histvestor_draft):
    inv1 = Investor.objects.get()
    assert [NAME, COMMENT, HOMEPAGE, OPENCORP] == [
        inv1.name,
        inv1.comment,
        inv1.homepage,
        inv1.opencorporates,
    ]
    assert inv1.country_id == 604
    assert inv1.classification == "PRIVATE_COMPANY"
    assert inv1.status == Investor.STATUS_DRAFT
    assert inv1.draft_status == 1
    versions = Version.objects.get_for_object_reference(Investor, 1)
    v1 = versions.get()
    assert v1.revision.comment == ACTION_COMM


def test_draft_update_draft(histvestor_draft):
    histvestor_draft.classification = 40
    histvestor_draft.action_comment = "Fix classification"
    histvestor_draft.fk_status_id = 1
    histvestor_draft.save(update_elasticsearch=False, trigger_gnd=True)

    inv1 = Investor.objects.get()
    assert inv1.classification == "INVESTMENT_FUND"
    assert inv1.status == Investor.STATUS_DRAFT
    assert inv1.draft_status == 1
    versions = Version.objects.get_for_object_reference(Investor, 1)
    assert versions.count() == 2
    assert versions[0].revision.comment == "Fix classification"
    assert versions[1].revision.comment == ACTION_COMM


def test_investor_draft_to_live(histvestor_draft_live):
    inv1 = Investor.objects.get()
    assert [NAME, COMMENT, HOMEPAGE, OPENCORP] == [
        inv1.name,
        inv1.comment,
        inv1.homepage,
        inv1.opencorporates,
    ]
    assert inv1.status == Investor.STATUS_LIVE
    assert inv1.draft_status is None
    versions = Version.objects.get_for_object_reference(Investor, 1)
    assert versions.count() == 2
    assert versions[0].field_dict["status"] == Investor.STATUS_LIVE
    assert versions[0].revision.comment == "Approved"
    assert versions[1].field_dict["status"] == Investor.STATUS_DRAFT


def test_investor_live_and_draft(histvestor_draft_live):
    new_name = "The Supreme Investor! tm"
    histvestor_draft_live.fk_status_id = 1
    histvestor_draft_live.name = new_name
    histvestor_draft_live.action_comment = "Some more changes draft"
    histvestor_draft_live.save(update_elasticsearch=False, trigger_gnd=True)

    inv1 = Investor.objects.get()
    assert inv1.status == Investor.STATUS_LIVE
    assert inv1.draft_status == 1
    assert inv1.name == NAME
    versions = Version.objects.get_for_object_reference(Investor, 1)
    assert versions.count() == 3
    assert versions[0].revision.comment == "Some more changes draft"
    assert versions[0].field_dict["status"] == Investor.STATUS_LIVE
    assert versions[0].field_dict["name"] == new_name

    histvestor_draft_live.fk_status_id = 2
    histvestor_draft_live.action_comment = "Approve changes"
    histvestor_draft_live.save(update_elasticsearch=False, trigger_gnd=True)

    inv1 = Investor.objects.get()
    assert inv1.status == Investor.STATUS_UPDATED
    assert inv1.draft_status is None
    assert inv1.name == new_name
    versions = Version.objects.get_for_object_reference(Investor, 1)
    assert versions.count() == 4
    assert versions[0].revision.comment == "Approve changes"
    assert versions[0].field_dict["status"] == Investor.STATUS_UPDATED
    assert versions[0].field_dict["name"] == new_name


@pytest.mark.django_db
def test_new_investor_live_directly():
    now = timezone.now()
    histvestor = HistoricalInvestor(
        investor_identifier=1,
        fk_status_id=Investor.STATUS_LIVE,
        name=NAME,
        classification=10,
        history_date=now,
        fk_country_id=604,
        comment=COMMENT,
        action_comment=ACTION_COMM,
    )
    histvestor.save(update_elasticsearch=False, trigger_gnd=True)
    assert HistoricalInvestor.objects.filter(investor_identifier=1).count() == 1

    inv1 = Investor.objects.get()
    assert inv1.status == Investor.STATUS_LIVE
    assert inv1.draft_status is None
    versions = Version.objects.get_for_object_reference(Investor, 1)
    v1 = versions.get()
    assert v1.revision.comment == ACTION_COMM


@pytest.mark.django_db
def test_new_investor_deleted_directly():
    now = timezone.now()
    histvestor = HistoricalInvestor(
        investor_identifier=1,
        fk_status_id=Investor.STATUS_DELETED,
        name=NAME,
        classification=10,
        history_date=now,
        fk_country_id=604,
        comment=COMMENT,
        action_comment=ACTION_COMM,
        homepage=HOMEPAGE,
        opencorporates_link=OPENCORP,
    )
    histvestor.save(update_elasticsearch=False, trigger_gnd=True)
    assert HistoricalInvestor.objects.filter(investor_identifier=1).count() == 1

    inv1 = Investor.objects.get()
    assert inv1.status == Investor.STATUS_DELETED
    assert inv1.draft_status is None
    versions = Version.objects.get_for_object_reference(Investor, 1)
    v1 = versions.get()
    assert v1.revision.comment == ACTION_COMM


def test_investor_live_then_delete(histvestor_draft_live):
    histvestor_draft_live.fk_status_id = Investor.STATUS_DELETED
    histvestor_draft_live.action_comment = "Delete this!"
    histvestor_draft_live.save(update_elasticsearch=False, trigger_gnd=True)

    inv1 = Investor.objects.get()
    assert inv1.status == Investor.STATUS_DELETED
    assert inv1.draft_status == None
    versions = Version.objects.get_for_object_reference(Investor, 1)
    assert versions.count() == 3
    assert versions[0].revision.comment == "Delete this!"
    assert versions[0].field_dict["status"] == Investor.STATUS_DELETED

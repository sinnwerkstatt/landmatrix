from datetime import datetime

import pytest
from django.utils import timezone

from apps.greennewdeal.models import Investor
from apps.landmatrix.models import HistoricalInvestor


@pytest.mark.django_db
def test_all_status_options():
    ID = 1  # Draft (Pending)
    now = timezone.now()
    histvestor = HistoricalInvestor(
        investor_identifier=ID,
        fk_status_id=2,
        name="The Grand Investor",
        classification=10,
        history_date=now,
        fk_country_id=604,
        comment="regular comment",
        action_comment="ACTION COMMENT!",
        homepage="http://grandinvestor.the",
        opencorporates_link="http://closed.com",
    )

    histvestor.save(update_elasticsearch=False)

    assert HistoricalInvestor.objects.filter(investor_identifier=ID).count() == 1
    inv1 = Investor.objects.get()
    assert inv1.name == "The Grand Investor"
    assert inv1.status == Investor.STATUS_LIVE

    #
    # deal_draft_only = Deal.objects.get(id=ID)
    # assert deal_draft_only.status == deal_draft_only.STATUS_DRAFT
    # versions = Version.objects.get_for_object(deal_draft_only)
    # assert len(versions) == 1
    # assert versions[0].field_dict["id"] == ID
    # assert versions[0].field_dict["status"] == deal_draft_only.STATUS_DRAFT
    #
    # ID = 2  # Live (Active)
    # HistoricalActivity(activity_identifier=ID, fk_status_id=2).save(
    #     update_elasticsearch=False
    # )
    # assert HistoricalActivity.objects.filter(activity_identifier=ID).count() == 1
    #
    # deal_live_only = Deal.objects.get(id=ID)
    # assert deal_live_only.status == deal_live_only.STATUS_LIVE
    # versions = Version.objects.get_for_object(deal_live_only)
    # assert len(versions) == 1
    # assert versions[0].field_dict["id"] == ID
    # assert versions[0].field_dict["status"] == deal_live_only.STATUS_LIVE
    #
    # ID = 3  # Live (this time with Overwritten)
    # HistoricalActivity(activity_identifier=ID, fk_status_id=3).save(
    #     update_elasticsearch=False
    # )
    # assert HistoricalActivity.objects.filter(activity_identifier=ID).count() == 1
    #
    # deal_live_only = Deal.objects.get(id=ID)
    # assert deal_live_only.status == deal_live_only.STATUS_LIVE
    # versions = Version.objects.get_for_object(deal_live_only)
    # assert len(versions) == 1
    # assert versions[0].field_dict["id"] == ID
    # assert versions[0].field_dict["status"] == deal_live_only.STATUS_LIVE
    #
    # # Stati: Deleted, Rejected, To Delete
    # for status in [4, 5, 6]:
    #     HistoricalActivity(activity_identifier=status, fk_status_id=status).save(
    #         update_elasticsearch=False
    #     )
    #     assert (
    #         HistoricalActivity.objects.filter(activity_identifier=status).count() == 1
    #     )
    #
    #     deal_live_only = Deal.objects.get(id=status)
    #     assert deal_live_only.status == status
    #     versions = Version.objects.get_for_object(deal_live_only)
    #     assert len(versions) == 1
    #     assert versions[0].field_dict["id"] == status
    #     assert versions[0].field_dict["status"] == status
    #

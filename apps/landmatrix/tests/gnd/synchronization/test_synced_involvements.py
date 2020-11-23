import pytest
from django.utils import timezone

from apps.landmatrix.models import (
    HistoricalInvestor,
    HistoricalInvestorVentureInvolvement,
    InvestorVentureInvolvement,
)
from apps.landmatrix.models import Investor
from apps.landmatrix.models.gndinvestor import (
    InvestorVersion,
    InvestorVentureInvolvementVersion,
)
from apps.landmatrix.models.versions import Version

NAME = "The Grand Investor"
COMMENT = "regular blabla comment"
HOMEPAGE = "https://grandinvestor.the"
OPENCORP = "http://closed.com"
ACTION_COMM = "AKTION!"


def test_histvolvement_draft(db):
    hi1 = HistoricalInvestor(investor_identifier=1, fk_status_id=Investor.STATUS_DRAFT)
    hi1.save(update_elasticsearch=False)
    hi2 = HistoricalInvestor(investor_identifier=2, fk_status_id=Investor.STATUS_DRAFT)
    hi2.save(update_elasticsearch=False)
    assert HistoricalInvestor.objects.all().count() == 2

    HistoricalInvestorVentureInvolvement.objects.create(
        fk_venture=hi1,
        fk_investor=hi2,
        role="ST",
    )
    hi1.save(update_elasticsearch=False)

    hi1.refresh_from_db()
    assert hi1.venture_involvements.all()  # yes, the naming is wrong.. old bug.

    assert [i.status for i in Investor.objects.all()] == [1, 1]
    ivi = InvestorVentureInvolvement.objects.get()
    assert ivi.venture.id == 1
    assert ivi.investor.id == 2

    assert ivi.venture.investors.all()
    assert ivi.investor.ventures.all()

    hi1 = HistoricalInvestor(investor_identifier=1, fk_status_id=Investor.STATUS_LIVE)
    hi1.save(update_elasticsearch=False)
    HistoricalInvestorVentureInvolvement.objects.create(
        fk_venture=hi1, fk_investor=hi2, role="ST", percentage=10.0
    )
    hi1.save(update_elasticsearch=False)

    i1 = Investor.objects.get(id=1)
    assert InvestorVentureInvolvement.objects.get(venture_id=i1.id).percentage == 10

    hi3 = HistoricalInvestor(investor_identifier=3, fk_status_id=Investor.STATUS_LIVE)
    hi3.save(update_elasticsearch=False)
    assert HistoricalInvestor.objects.all().count() == 4
    HistoricalInvestorVentureInvolvement.objects.create(
        fk_venture=hi1, fk_investor=hi3, role="ST", percentage=60
    )
    hi1.save()

    assert InvestorVentureInvolvement.objects.filter(venture_id=i1.id).count() == 2

    hi1 = HistoricalInvestor(investor_identifier=1, fk_status_id=Investor.STATUS_DRAFT)
    hi1.save(update_elasticsearch=False)
    HistoricalInvestorVentureInvolvement.objects.create(
        fk_venture=hi1, fk_investor=hi2, role="ST", percentage=20.0
    )
    hi1.save(update_elasticsearch=False)
    involves = InvestorVentureInvolvement.objects.filter(venture_id=i1.id)
    assert {x.percentage for x in involves} == {10, 60}

    hi1 = HistoricalInvestor(
        investor_identifier=1, fk_status_id=Investor.STATUS_DELETED
    )
    hi1.save(update_elasticsearch=False)

    assert not InvestorVentureInvolvement.objects.filter(venture_id=i1.id).exists()

    # ivi_vs = InvestorVentureInvolvementVersion.objects.all()
    # print([x.object_id for x in ivi_vs])
    # xx = ivi_vs[0]
    # print(xx.fields)
    # print(xx)

import freezegun
from django.db.models import Q
from django.utils import timezone

from apps.landmatrix.models.country import Region
from apps.landmatrix.models.quality_indicators import (
    DealQISnapshot,
    create_deal_qi_counts,
    create_investor_qi_counts,
    create_counts,
)

from apps.landmatrix.quality_indicators import DEAL_QIS, INVESTOR_QIS
from apps.landmatrix.quality_indicators.dataclass import QualityIndicator


@freezegun.freeze_time("2024-09-26T13:59:01")
def test_deal_create_defaults():
    snap = DealQISnapshot.objects.create()

    assert snap.created_at == timezone.now(), "Tz-aware timestamp set to now."

    assert snap.region is None, "Default region is None."
    assert snap.subset_key is None, "Default subset is None."

    assert snap.data == {}, "Default data is empty dict."


def test_deal_create():
    ASIA = Region.objects.get(name="Asia")

    snap = DealQISnapshot.objects.create(
        region=ASIA,
        subset_key="MY_SUBSET",
    )

    assert snap.region == ASIA, "Region is Asia."
    assert snap.subset_key == "MY_SUBSET", "Subset is mine."


def test_create_deal_snapshot():
    data = create_deal_qi_counts(None, None)

    assert all(qi.key in data.keys() for qi in DEAL_QIS)


def test_create_investor_snapshot():
    data = create_investor_qi_counts()

    assert all(qi.key in data.keys() for qi in INVESTOR_QIS)


# TODO: Use dedicated test model and actually test non-trivial Qs
def test_create_counts():
    assert list(create_counts([]).keys()) == ["TOTAL"]

    qis = [
        QualityIndicator("GREEN_DEAL", "Green deals", "Green is the color of hope", Q),
        QualityIndicator("BLUE_DEAL", "Blue deals", "Blue is the color of calm", Q),
        QualityIndicator("RED_DEAL", "Red deals", "Red is the color of hate", Q),
    ]

    assert list(create_counts(qis).keys()) == [
        "TOTAL",
        "GREEN_DEAL",
        "BLUE_DEAL",
        "RED_DEAL",
    ]

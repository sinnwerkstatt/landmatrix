from apps.landmatrix.models.choices import (
    InvolvementRoleEnum,
    InvestmentTypeEnum,
    ParentRelationEnum,
)
from apps.landmatrix.models.currency import Currency
from apps.landmatrix.models.investor import InvestorHull, Involvement
from apps.landmatrix.serializers import InvolvementSerializer


def test_involvement_serializer_empty():
    child = InvestorHull.objects.create(id=500)
    parent = InvestorHull.objects.create(id=501)

    involvement = Involvement.objects.create(
        id=22,
        child_investor=child,
        parent_investor=parent,
    )

    assert InvolvementSerializer(involvement).data == {
        "id": 22,
        "nid": involvement.nid,
        "child_investor_id": 500,
        "parent_investor_id": 501,
        "role": "",
        "investment_type": [],
        "percentage": None,
        "loans_amount": None,
        "loans_currency_id": None,
        "loans_date": None,
        "parent_relation": None,
        "comment": "",
    }


def test_involvement_serializer_all():
    child = InvestorHull.objects.create(id=500)
    parent = InvestorHull.objects.create(id=501)

    involvement = Involvement.objects.create(
        id=22,
        nid="22_super",
        child_investor=child,
        parent_investor=parent,
        role=InvolvementRoleEnum.PARENT,
        investment_type=[
            InvestmentTypeEnum.DEBT_FINANCING,
            InvestmentTypeEnum.EQUITY,
        ],
        percentage=79.22,
        loans_amount=123.01,
        loans_currency=Currency.objects.create(id=66, name="money", ranking=1),
        loans_date="2024-01-01",
        parent_relation=ParentRelationEnum.LOCAL_BRANCH,
        comment="The have a strong bound (through money).",
    )

    assert InvolvementSerializer(involvement).data == {
        "id": 22,
        "nid": "22_super",
        "child_investor_id": 500,
        "parent_investor_id": 501,
        "role": InvolvementRoleEnum.PARENT,
        "investment_type": [
            InvestmentTypeEnum.DEBT_FINANCING,
            InvestmentTypeEnum.EQUITY,
        ],
        "percentage": "79.22",
        "loans_amount": 123.01,
        "loans_currency_id": 66,
        "loans_date": "2024-01-01",
        "parent_relation": ParentRelationEnum.LOCAL_BRANCH,
        "comment": "The have a strong bound (through money).",
    }

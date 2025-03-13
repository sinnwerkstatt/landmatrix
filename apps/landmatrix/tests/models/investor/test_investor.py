from apps.landmatrix.models.abstract import VersionStatus
from apps.landmatrix.models.choices import InvolvementRoleEnum
from apps.landmatrix.models.investor import InvestorHull, InvestorVersion, Involvement
from apps.landmatrix.serializers import InvolvementSerializer


def test_apply_snapshot():
    i1: InvestorHull = InvestorHull.objects.create()
    i2: InvestorHull = InvestorHull.objects.create()
    i3: InvestorHull = InvestorHull.objects.create()

    old_involvement: Involvement = Involvement.objects.create(
        parent_investor=i1,
        child_investor=i2,
        role=InvolvementRoleEnum.PARENT,
    )

    new_involvements: list[Involvement] = [
        Involvement(
            parent_investor=i1,
            child_investor=i2,
            role=InvolvementRoleEnum.LENDER,
        ),
        Involvement(
            parent_investor=i1,
            child_investor=i3,
            role=InvolvementRoleEnum.PARENT,
        ),
    ]

    version = InvestorVersion.objects.create(
        investor=i2,
        name="Test Child Investor",
        status=VersionStatus.ACTIVATION,
        involvements_snapshot=InvolvementSerializer(
            new_involvements,
            many=True,
        ).data,
    )

    version._apply_snapshot()

    assert Involvement.objects.count() == 2
    assert (
        Involvement.objects.filter(
            child_investor=i2,
            parent_investor=i1,
            role=InvolvementRoleEnum.LENDER,
        ).count()
        == 1
    ), "Single unique involvement of parent and child."

    assert not Involvement.objects.filter(pk=old_involvement.pk).exists(), (
        "Deletes old involvement"
    )

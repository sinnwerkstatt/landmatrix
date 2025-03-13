from apps.landmatrix.models.choices import InvolvementRoleEnum
from apps.landmatrix.models.investor import InvestorHull, InvestorVersion, Involvement
from apps.landmatrix.serializers import InvolvementSerializer


def test_apply_snapshot():
    i1: InvestorHull = InvestorHull.objects.create()  # Parent/Lender 1
    i2: InvestorHull = InvestorHull.objects.create()  # Child

    involvement: Involvement = Involvement.objects.create(
        parent_investor=i1,
        child_investor=i2,
        role=InvolvementRoleEnum.PARENT,
    )

    involvements_snap: list[Involvement] = [
        Involvement(
            parent_investor=i1,
            child_investor=i2,
            role=InvolvementRoleEnum.LENDER,
        ),
    ]

    version = InvestorVersion.objects.create(
        investor=i2,
        involvements_snapshot=InvolvementSerializer(
            involvements_snap,
            many=True,
        ).data,
    )

    version._apply_snapshot()

    assert Involvement.objects.count() == 1
    assert not Involvement.objects.filter(pk=involvement.pk).exists()


def test_apply_snapshot_updates_existing_involvements():
    i1: InvestorHull = InvestorHull.objects.create()  # Parent/Lender 1
    i2: InvestorHull = InvestorHull.objects.create()  # Parent/Lender 2
    i3: InvestorHull = InvestorHull.objects.create()  # Child

    involvement = Involvement.objects.create(
        parent_investor=i1,
        child_investor=i3,
    )

    involvements_snap: list[Involvement] = [
        Involvement(
            id=involvement.id,  # has id
            parent_investor=i2,
            child_investor=i3,
        )
    ]

    version = InvestorVersion.objects.create(
        investor=i3,
        involvements_snapshot=InvolvementSerializer(
            involvements_snap,
            many=True,
        ).data,
    )

    version._apply_snapshot()

    assert Involvement.objects.count() == 1
    assert Involvement.objects.filter(pk=involvement.pk).exists()

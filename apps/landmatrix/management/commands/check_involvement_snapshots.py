from django.core.management import BaseCommand

from apps.landmatrix.models.investor import InvestorHull, InvestorVersion


class Command(BaseCommand):
    help = "Check involvement snapshot integrity."

    def handle(self, *args, **options):
        print("Checking involvement snapshots...")
        print("investorID", "versionID", "invParentID", "invChildID")
        for v in InvestorVersion.objects.all():
            for inv in v.involvements_snapshot:
                try:
                    assert inv["nid"] is not None  # noqa: S101
                    assert inv["child_investor_id"] == v.investor_id  # noqa: S101
                except AssertionError:
                    print(
                        v.investor_id,
                        v.id,
                        inv["parent_investor_id"],
                        inv["child_investor_id"],
                    )
                    pass

        print("Checking involvement models...")
        for i in InvestorHull.objects.all():
            parent_ids = [p.id for p in i.get_parents()]
            parent_nids = [p.nid for p in i.get_parents()]
            try:
                assert all(parent_nids)  # noqa: S101
            except AssertionError:
                print(i.id)

            if v := i.active_version:
                invos = v.involvements_snapshot
                try:
                    assert len(parent_ids) == len(invos)  # noqa: S101
                    assert set(parent_ids) == {p["id"] for p in invos}  # noqa: S101
                except AssertionError:
                    print(i.id, v.id)

        print("DONE")

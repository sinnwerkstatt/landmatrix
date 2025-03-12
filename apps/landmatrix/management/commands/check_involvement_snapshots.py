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
            parents = [p.id for p in i.get_parents()]

            if v := i.active_version:
                invos = v.involvements_snapshot
                try:
                    assert len(parents) == len(invos)  # noqa: S101
                    assert set(parents) == {p["id"] for p in invos}  # noqa: S101
                except AssertionError:
                    print(i.id, v.id)

        print("DONE")

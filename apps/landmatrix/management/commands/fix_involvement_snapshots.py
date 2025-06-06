from tqdm import tqdm

from django.core.management import BaseCommand
from django.db.models import QuerySet

from apps.landmatrix.management.helpers import db_require_confirmation
from apps.landmatrix.models.choices import InvolvementRoleEnum
from apps.landmatrix.models.investor import InvestorHull, Involvement
from apps.landmatrix.nid import generate_nid


class Command(BaseCommand):
    help = "Fix involvement snapshots nano ids."

    @db_require_confirmation
    def handle(self, *args, **options):
        qs: QuerySet[InvestorHull] = InvestorHull.objects.all()

        print("Iterating InvestorHulls.")
        for obj in tqdm(qs.iterator(), total=qs.count()):
            for version in obj.versions.all():
                # active_version.involvements_snapshot can be reset, because new
                # derived version initiate with database involvements.
                if version.id == obj.active_version_id:
                    version.involvements_snapshot = version._create_snapshot()
                    version.save()
                    continue

                snapshot = version.involvements_snapshot

                # Only keep involvements where current investor is child investor
                snapshot = [i for i in snapshot if i["child_investor_id"] == obj.id]

                # Only keep involvements with non-empty parent investor
                snapshot = [i for i in snapshot if i["parent_investor_id"] is not None]

                # Only keep involvements with valid role
                snapshot = [i for i in snapshot if i["role"] in InvolvementRoleEnum]

                # Only keep unique parent investors
                parent_ids = [s["parent_investor_id"] for s in snapshot]
                snapshot = [
                    x
                    for i, x in enumerate(snapshot)
                    if i == parent_ids.index(x["parent_investor_id"])
                ]

                # Patch involvement ids
                for inv in snapshot:
                    try:
                        match = Involvement.objects.get(
                            child_investor_id=obj.id,
                            parent_investor_id=inv["parent_investor_id"],
                        )
                        inv["id"] = match.id
                        inv["nid"] = match.nid
                    except Involvement.DoesNotExist:
                        inv["id"] = None
                        inv["nid"] = generate_nid(Involvement)

                assert all(snap["nid"] for snap in snapshot)  # noqa: S101

                # Set and save snapshot
                version.involvements_snapshot = snapshot
                version.save()

        print("DONE")

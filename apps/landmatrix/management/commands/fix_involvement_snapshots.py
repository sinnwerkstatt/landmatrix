import re
from typing import cast

from tqdm import tqdm

from django.core.management import BaseCommand
from apps.landmatrix.models.investor import InvestorHull, Involvement
from apps.landmatrix.nid import generate_nid


class Command(BaseCommand):
    def handle(self, *args, **options):
        confirm = input(
            "***** ATTENTION ***** \n"
            "This command potentially manipulates DB. \n"
            "Make sure DB connection is configured correctly in .env. \n"
            "Confirm to continue (y/N): "
        )

        if not confirm or not re.match("^y(es)?$", confirm, re.I):
            print("Aborting")
            return

        qs = InvestorHull.objects.all()
        qs_iterator = map(lambda x: cast(InvestorHull, x), qs.iterator())

        print("Iterating InvestorHulls.")
        for obj in tqdm(qs_iterator, total=qs.count()):

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

                assert all(snap["nid"] for snap in snapshot)

                # Set and save snapshot
                version.involvements_snapshot = snapshot
                version.save()

        print("DONE")

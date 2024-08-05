import re

from tqdm import tqdm

from django.core.management import BaseCommand
from apps.landmatrix.models.new import InvestorHull, Involvement
from apps.landmatrix.nid import generate_nid

# Questions:
# - should snapshot include child or parent or both involvements?
# -> I decide for only parent and ALWAYS QUERY child for display!
# - how to deal with parent_investor is None? -> Ignore

qs_values = Involvement.objects.values(
    "id",
    "nid",
    "parent_investor_id",
    "child_investor_id",
    "role",
    "investment_type",
    "percentage",
    "loans_amount",
    "loans_currency_id",
    "loans_date",
    "parent_relation",
    "comment",
).order_by("id")


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

        # Filter out deleted ones, because they have status issues
        qs = InvestorHull.objects.filter(deleted=False)

        print("Iterating InvestorHulls.")
        for obj in tqdm(qs.iterator(), total=qs.count()):

            qs_involvements = qs_values.filter(child_investor_id=obj.id)

            for version in obj.versions.all():

                # active_version.involvements_snapshot can be reset, because new
                # derived version initiate with database involvements.
                if version.id == obj.active_version_id:
                    # manually serialize percentage value
                    version.involvements_snapshot = [
                        {
                            **inv,
                            "percentage": (
                                float(inv["percentage"])
                                if inv["percentage"] is not None
                                else None
                            ),
                        }
                        for inv in qs_involvements
                    ]
                    version.save()
                    continue

                snapshot = version.involvements_snapshot

                # This is bad: There are some involvements with missing parent_investor_id
                # How to proceed? Delete? Ignore them for now!
                snapshot = [i for i in snapshot if i["parent_investor_id"] is not None]
                # print("1", snapshot)

                # Only keep child investor relations
                snapshot = [i for i in snapshot if i["child_investor_id"] == obj.id]
                # print("2", snapshot)

                # Only keep unique parent investors
                parent_ids = [s["parent_investor_id"] for s in snapshot]
                snapshot = [
                    x
                    for i, x in enumerate(snapshot)
                    if i == parent_ids.index(x["parent_investor_id"])
                ]
                # print("3", snapshot)

                for inv in snapshot:
                    qs_match = qs_involvements.filter(
                        parent_investor_id=inv["parent_investor_id"],
                    )

                    if qs_match.exists():
                        match = qs_match.first()
                        inv["id"] = match["id"]
                        inv["nid"] = match["nid"]
                    else:
                        inv["id"] = None
                        inv["nid"] = generate_nid(Involvement)
                        # print("NO MATCH", obj, version)

                assert all(snap["nid"] for snap in snapshot)
                version.involvements_snapshot = snapshot
                version.save()

        print("DONE")

import re

from tqdm import tqdm

from django.core.management import BaseCommand

from apps.landmatrix.models.abstract import VersionStatus
from apps.landmatrix.models.deal import DealHull, DealVersion
from apps.landmatrix.models.investor import InvestorHull, InvestorVersion


class Command(BaseCommand):
    help = "Check status integrity of all deals and investors."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fix",
            action="store_true",
            help="Fix active and draft version foreign keys.",
        )

    def handle(self, *args, **options):
        if options["fix"]:
            confirm = input(
                "***** ATTENTION ***** \n"
                "This command potentially manipulates DB. \n"
                "Make sure DB connection is configured correctly in .env. \n"
                "Confirm to continue (y/N): "
            )

            if not confirm or not re.match("^y(es)?$", confirm, re.I):
                print("Aborting")
                return

        # TODO: Check if two versions are 'equal'
        # v1 = d1.versions.values('id', ...).first()
        # d1.versions.exclude(id=v1['id']).filter(**v1).exists()

        for model in [DealHull, InvestorHull]:
            qs = model.objects.order_by("id").all()

            count_fixed = 0
            print(f"Iterating {model.__name__}s.")
            for obj in tqdm(qs.iterator(), total=qs.count()):
                needs_fixing = False

                active_version, draft_version = find_active_and_draft_version(obj)

                if obj.active_version != active_version:
                    # print("Wrong active version for", obj)
                    obj.active_version = active_version
                    needs_fixing = True

                if obj.draft_version != draft_version:
                    # print("Wrong draft version for", obj)
                    obj.draft_version = draft_version
                    needs_fixing = True

                if needs_fixing:
                    count_fixed += 1

                    if options["fix"]:
                        # print("Fixing...")
                        obj.save()

            if options["fix"]:
                print(f"Fixed {count_fixed} {model.__name__}s.")
            else:
                print(f"{count_fixed} {model.__name__}s need fixing.")

            print()

        print("DONE")


def find_active_and_draft_version(
    obj: DealHull | InvestorHull,
) -> tuple[
    DealVersion | InvestorVersion | None,
    DealVersion | InvestorVersion | None,
]:
    qs_versions = obj.versions.order_by("id")

    active_version = qs_versions.filter(status=VersionStatus.ACTIVATED).last()

    draft_version = (
        qs_versions
        # --
        .filter(id__gt=(active_version.id if active_version else -1))
        .exclude(status=VersionStatus.ACTIVATED)
        .last()
    )
    return active_version, draft_version

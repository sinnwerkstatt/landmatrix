from django.core.management.base import BaseCommand

from apps.landmatrix.models import (
    HistoricalActivity,
    Deal,
)
from apps.landmatrix.models.deal import (
    DealTopInvestors,
    DealParentCompanies,
    DealWorkflowInfo,
)
from apps.landmatrix.models.versions import Revision
from apps.landmatrix.synchronization.deal import histivity_to_deal


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--rewrite-deals", action="store_true")
        parser.add_argument("--ignore-history", action="store_true")
        parser.add_argument("deal_ids", nargs="*", type=int)

    def handle(self, *args, **options):
        deal_ids = HistoricalActivity.objects.values_list(
            "activity_identifier", flat=True
        )
        # deal_ids = deal_ids.filter(activity_identifier__gte=958)
        if options["deal_ids"]:
            deal_ids = deal_ids.filter(activity_identifier__in=options["deal_ids"])
        deal_ids = deal_ids.distinct().order_by("activity_identifier")
        if options["ignore_history"]:
            print(
                "\n\n\nATTENTION. We're just syncing the last version of each Deal now!!!\n\n\n"
            )
        for deal_id in deal_ids:
            if options["rewrite_deals"]:
                print(f"  Removing Deal {deal_id}... ", end="", flush=True)
                Revision.objects.filter(dealversion__object_id=deal_id).delete()
                Deal.objects.filter(id=deal_id).delete()
                print("\033[92m" + "OK" + "\033[0m")

            print(f"  Sync Deal {deal_id}... ", end="", flush=True)
            if options["ignore_history"]:
                histivity_id = (
                    HistoricalActivity.objects.filter(activity_identifier=deal_id)
                    .order_by("-id")
                    .values_list("id", flat=True)
                )[0]
                histivity_to_deal(activity_pk=histivity_id)
            else:
                histivity_to_deal(activity_identifier=deal_id)
            print("\033[92m" + "OK" + "\033[0m")

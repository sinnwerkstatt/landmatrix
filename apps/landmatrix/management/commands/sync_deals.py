from django.core.management.base import BaseCommand

from apps.landmatrix.models import HistoricalActivity
from apps.landmatrix.synchronization.deal import histivity_to_deal


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--rewrite-deals", action="store_true")

    def handle(self, *args, **options):
        print("rewrite_deals", options["rewrite_deals"])
        # if options["rewrite_deals"]:
        #     Revision.objects.filter(dealversion__object_id=4).delete()
        deal_ids = (
            HistoricalActivity.objects.values_list("activity_identifier", flat=True)
            # .filter(activity_identifier__gte=1890)
            .distinct().order_by("activity_identifier")
        )
        for histivity_identifier in deal_ids:
            print(f"  Sync Deal {histivity_identifier}... ", end="", flush=True)
            histivity_to_deal(activity_identifier=histivity_identifier)
            print("\033[92m" + "OK" + "\033[0m")

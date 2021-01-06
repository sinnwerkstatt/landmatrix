from django.core.management.base import BaseCommand

from apps.landmatrix.models import (
    HistoricalActivity,
    Deal,
    Location,
    DataSource,
    Contract,
)
from apps.landmatrix.models.deal import DealTopInvestors, DealParentCompanies
from apps.landmatrix.models.versions import Revision
from apps.landmatrix.synchronization.deal import histivity_to_deal


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--rewrite-deals", action="store_true")

    def handle(self, *args, **options):
        deal_ids = (
            HistoricalActivity.objects.values_list("activity_identifier", flat=True)
            # .filter(activity_identifier=2)
            .distinct().order_by("activity_identifier")
        )
        for deal_id in deal_ids:
            if options["rewrite_deals"]:
                print(f"  Removing Deal {deal_id}... ", end="", flush=True)
                Revision.objects.filter(dealversion__object_id=deal_id).delete()
                DealTopInvestors.objects.filter(deal_id=deal_id).delete()
                DealParentCompanies.objects.filter(deal_id=deal_id).delete()
                Location.objects.filter(deal_id=deal_id).delete()
                DataSource.objects.filter(deal_id=deal_id).delete()
                Contract.objects.filter(deal_id=deal_id).delete()
                Deal.objects.filter(id=deal_id).delete()
                print("\033[92m" + "OK" + "\033[0m")

            print(f"  Sync Deal {deal_id}... ", end="", flush=True)
            histivity_to_deal(activity_identifier=deal_id)
            print("\033[92m" + "OK" + "\033[0m")

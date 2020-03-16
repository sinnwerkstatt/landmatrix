from django.core.management.base import BaseCommand

from apps.greennewdeal.synchronization.deal import histivity_to_deal
from apps.landmatrix.models import HistoricalActivity


class Command(BaseCommand):
    def handle(self, *args, **options):
        deal_ids = (
            HistoricalActivity.objects.values_list("activity_identifier", flat=True)
            # .filter(activity_identifier__gt=7700)
            .distinct().order_by("activity_identifier")
        )
        for histivity_identifier in deal_ids:
            print(f"  Sync Deal {histivity_identifier}... ", end="", flush=True)
            histivity_to_deal(activity_identifier=histivity_identifier)
            print("\033[92m" + "OK" + "\033[0m")

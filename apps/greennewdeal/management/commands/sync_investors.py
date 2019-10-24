from django.core.management.base import BaseCommand

from apps.greennewdeal.synchronization.investor import histvestor_to_investor
from apps.landmatrix.models import HistoricalInvestor


class Command(BaseCommand):
    def handle(self, *args, **options):
        hinv_ids = (
            HistoricalInvestor.objects.values_list("investor_identifier", flat=True)
            .distinct()
            .order_by("investor_identifier")
        )
        for investor_identifier in hinv_ids:
            print(f"  Sync Investor {investor_identifier}... ", end="", flush=True)
            histvestor_to_investor(investor_identifier=investor_identifier)
            print("\033[92m" + "OK" + "\033[0m")

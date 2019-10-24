from django.core.management.base import BaseCommand

from apps.greennewdeal.synchronization.investor import sync_involvements
from apps.landmatrix.models import HistoricalInvestorVentureInvolvement


class Command(BaseCommand):
    def handle(self, *args, **options):
        ids_groups = (
            HistoricalInvestorVentureInvolvement.objects.values_list(
                "fk_venture__investor_identifier", "fk_investor__investor_identifier"
            )
            .distinct()
            .order_by(
                "fk_venture__investor_identifier", "fk_investor__investor_identifier"
            )
        )
        for ids in ids_groups:
            print(f"  Sync Involvement {ids}... ", end="", flush=True)
            sync_involvements(ids)
            print("\033[92m" + "OK" + "\033[0m")

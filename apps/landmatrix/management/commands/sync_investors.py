from django.core.management.base import BaseCommand

from apps.landmatrix.models import Investor
from apps.landmatrix.synchronization.investor import histvestor_to_investor
from apps.landmatrix.models import HistoricalInvestor


class Command(BaseCommand):
    def handle(self, *args, **options):
        histvestor_versions = (
            HistoricalInvestor.objects.all()
            # .filter(investor_identifier=204)
            .order_by("pk")
        )
        total = histvestor_versions.count()
        i = 1
        for histvestor in histvestor_versions:
            print(f"\r> {i}/{total}", end="")
            i += 1
            histvestor_to_investor(histvestor)

from django.core.management.base import BaseCommand

from apps.greennewdeal.models import Investor
from apps.greennewdeal.synchronization.investor import hist_to_inv
from apps.landmatrix.models import HistoricalInvestor


class Command(BaseCommand):
    def handle(self, *args, **options):
        histvestor_versions = HistoricalInvestor.objects.all().order_by("pk")
        total = histvestor_versions.count()
        i = 1
        for histvestor in histvestor_versions:
            print(f"\r> {i}/{total}", end="")
            i += 1
            try:
                Investor.objects.get(old_id=histvestor.id)
            except Investor.DoesNotExist:
                hist_to_inv(histvestor)

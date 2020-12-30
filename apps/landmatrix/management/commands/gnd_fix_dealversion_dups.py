from collections import Counter

from django.core.management.base import BaseCommand

from apps.landmatrix.models import HistoricalActivity, HistoricalInvestor, Deal
from apps.landmatrix.models.deal import DealVersion
from apps.landmatrix.models.gndinvestor import InvestorVersion


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Activities")

        for deal in Deal.objects.all().order_by("pk")[:5]:
            print(f"Deal #{deal.id}")
            version_timestamps = set()
            for dv in DealVersion.objects.filter(object_id=deal.id):
                if dv.revision.date_created in version_timestamps:
                    print("we probably already have this one:")
                    print(dv.revision.date_created)

                else:
                    version_timestamps.add(dv.revision.date_created)

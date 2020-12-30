from collections import Counter

from django.core.management.base import BaseCommand

from apps.landmatrix.models import HistoricalActivity, HistoricalInvestor, Deal
from apps.landmatrix.models.gndinvestor import InvestorVersion


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Activities")

        sql_attempt = """
            select * from (
              SELECT id,
              ROW_NUMBER() OVER(PARTITION BY serialized_data ORDER BY id asc) AS Row
              FROM landmatrix_investorversion
            ) dups
            where
            dups.Row > 1
            """
        for inversion in InvestorVersion.objects.all():
            print(inversion)

from django.core.management import BaseCommand

from apps.landmatrix.models import DealQISnapshot, InvestorQISnapshot
from apps.landmatrix.models.country import Region
from apps.landmatrix.models.quality_indicators import (
    create_deal_qi_counts,
    create_investor_qi_counts,
)
from apps.landmatrix.quality_indicators.deal import DEAL_SUBSETS


class Command(BaseCommand):
    help = "Compute and store Quality Indicator statistics."

    def handle(self, *args, **options):
        create_deal_qi_snapshots()
        create_investor_qi_snapshots()


def create_deal_qi_snapshots():
    print("Creating Deal QI snapshots...")

    for region in [*Region.objects.all(), None]:
        print(f"Region: {region or 'global'}")

        for subset_key in [x.key for x in DEAL_SUBSETS] + [None]:
            print(f"\tSubset: {subset_key or 'ALL'}")

            DealQISnapshot.objects.create(
                region=region,
                subset_key=subset_key,
                data=create_deal_qi_counts(region, subset_key),
            )

        print()


def create_investor_qi_snapshots():
    print("Creating Investor QI snapshots...")

    InvestorQISnapshot.objects.create(
        data=create_investor_qi_counts(),
    )

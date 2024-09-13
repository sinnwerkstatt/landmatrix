from django.core.management import BaseCommand

from apps.landmatrix.models.deal import DealVersion
from apps.landmatrix.models.investor import InvestorVersion


class Command(BaseCommand):
    def handle(self, *args, **options):
        for model in [InvestorVersion, DealVersion]:
            print(f"Iterating {model.__name__}s.")

            qs = model.objects.filter(
                created_at__isnull=False,
                modified_at__isnull=True,
            )
            for version in qs:
                version.modified_at = version.created_at
                version.save()

            print(f"Fixed {qs.count()} modification dates.")

            qs = model.objects.filter(
                created_by__isnull=False,
                modified_by__isnull=True,
            )
            for version in qs:
                version.modified_by = version.created_by
                version.save()

            print(f"Fixed {qs.count()} modification users.")
            print()

        print("DONE")

from django.core.management import BaseCommand
from django.db.models import Q

from apps.landmatrix.management.helpers import db_require_confirmation
from apps.landmatrix.models.abstract import VersionStatus
from apps.landmatrix.models.deal import DealHull
from apps.landmatrix.models.investor import InvestorHull


class Command(BaseCommand):
    help = "Fix version status (inverse of check_status_integrity)."

    @db_require_confirmation
    def handle(self, *args, **options):
        for model in [InvestorHull, DealHull]:
            print(f"Iterating {model.__name__}s.")

            qs = model.objects.filter(
                Q(active_version__isnull=False)
                & ~Q(active_version__status=VersionStatus.ACTIVATED)
                # & Q(deleted=True)
            )
            print(f"Fixing {qs.count()} active versions.")

            for obj in qs:
                obj.active_version.status = VersionStatus.ACTIVATED
                obj.active_version.save()
                obj.save()

            qs = model.objects.filter(
                Q(draft_version__isnull=False)
                & Q(draft_version__status=VersionStatus.ACTIVATED)
                # & Q(deleted=True)
            )
            print(f"Fixing {qs.count()} draft versions.")

            for obj in qs:
                obj.draft_version.status = VersionStatus.DRAFT
                obj.draft_version.save()
                obj.save()

            print()

        print("DONE")

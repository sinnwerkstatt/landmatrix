from django.core.management import BaseCommand
from django.db.models import Q

from apps.landmatrix.management.helpers import db_require_confirmation
from apps.landmatrix.models.deal import DealVersion


class Command(BaseCommand):
    help = "Recalculate public visible deals."

    @db_require_confirmation
    def handle(self, *args, **options):
        qs = DealVersion.objects.filter(is_public=True).filter(
            Q(operating_company__deleted=True)
            | Q(operating_company__active_version__isnull=True),
        )

        print(f"Fixing {qs.count()} deal versions.")

        for deal_version in qs:
            deal_version.save()

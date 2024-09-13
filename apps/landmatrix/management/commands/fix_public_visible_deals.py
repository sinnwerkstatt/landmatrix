import re

from django.core.management import BaseCommand
from django.db.models import Q

from apps.landmatrix.models.deal import DealVersion


class Command(BaseCommand):
    def handle(self, *args, **options):
        confirm = input(
            "***** ATTENTION ***** \n"
            "This command potentially manipulates DB. \n"
            "Make sure DB connection is configured correctly in .env. \n"
            "Confirm to continue (y/N): "
        )

        if not confirm or not re.match("^y(es)?$", confirm, re.I):
            print("Aborting")
            return

        qs = DealVersion.objects.filter(is_public=True).filter(
            Q(operating_company__deleted=True)
            | Q(operating_company__active_version__isnull=True),
        )

        print(f"Fixing {qs.count()} deal versions.")

        for deal_version in qs:
            deal_version.save()

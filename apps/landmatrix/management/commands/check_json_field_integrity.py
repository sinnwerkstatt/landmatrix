import re

from tqdm import tqdm

from django.core.management import BaseCommand

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

        total = DealVersion.objects.count()
        iterator = DealVersion.objects.iterator()

        print("Iterating DealVersions.")
        for version in tqdm(iterator, total=total):
            try:
                version._recalculate_fields()
            except:
                # recalculate deals prints debug info
                pass

        print("DONE")

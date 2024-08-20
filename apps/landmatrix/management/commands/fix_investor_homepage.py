import re

from django.core.management import BaseCommand

from apps.landmatrix.models.investor import InvestorVersion

ids = [
    3390,
    3391,
    3573,
    # 23678,
    23717,
    23741,
    23765,
    23809,
    23837,
    24485,
    24527,
    24646,
    24711,
]


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

        # this one has a completely wrong url -> reset
        v = InvestorVersion.objects.get(id=23678)
        v.homepage = ""
        v.save()

        # others have trailing or leading whitespaces or missing protocol
        for v in InvestorVersion.objects.filter(id__in=ids):
            v.homepage = v.homepage.strip()

            if not v.homepage.startswith("http"):
                v.homepage = "https://" + v.homepage

            v.save()

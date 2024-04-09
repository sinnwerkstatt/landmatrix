from django.core.management.base import BaseCommand

from apps.landmatrix.models.country import Country
from apps.landmatrix.models.deal import DealOld


#todo: exchange OldDeal?!

class Command(BaseCommand):
    def handle(self, *args, **options):
        countries = {
            x["id"]: x["name"] for x in Country.objects.all().values("id", "name")
        }
        for deal in DealOld.objects.all().order_by("id"):
            cntrs = set()
            for deal_version in deal.versions.all().order_by("id"):
                payload = deal_version.serialized_data
                if payload["country"]:
                    cntrs.add(payload["country"])
            if len(cntrs) > 1:
                print(
                    "|",
                    deal.id,
                    "|",
                    [countries[x] for x in cntrs],
                    "|",
                    f"https://landmatrix.org/deal/{deal.id}",
                    "|",
                )

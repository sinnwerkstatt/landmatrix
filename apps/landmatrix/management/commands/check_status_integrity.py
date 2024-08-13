from django.core.management import BaseCommand

from apps.landmatrix.models.deal import DealHull
from apps.landmatrix.models.investor import InvestorHull


class Command(BaseCommand):
    def handle(self, *args, **options):

        for model in [InvestorHull, DealHull]:
            print(f"Iterating {model.__name__}s.")

            for obj in model.objects.filter(deleted=False):
                if obj.active_version is not None:
                    version = obj.active_version
                    if not version.status == "ACTIVATED":
                        print("should be active:", obj, version, version.status)

                if obj.draft_version is not None:
                    version = obj.draft_version
                    if version.status == "ACTIVATED":
                        print("should be draft:", obj, version, version.status)
            print()

        print("DONE")

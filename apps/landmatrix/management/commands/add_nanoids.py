from django.core.management.base import BaseCommand

from apps.landmatrix.models import Deal

from nanoid import generate


class Command(BaseCommand):
    def handle(self, *args, **options):
        for deal in Deal.objects.all().order_by("id"):
            print(deal.id)
            for x in deal.locations:
                if not x.get("id") or isinstance(x["id"], int):
                    x["id"] = generate(size=8)
            for x in deal.datasources:
                if not x.get("id") or isinstance(x["id"], int):
                    x["id"] = generate(size=8)

            for x in deal.contracts:
                if not x.get("id") or isinstance(x["id"], int):
                    x["id"] = generate(size=8)

            deal.save()

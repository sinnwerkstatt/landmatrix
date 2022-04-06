from django.core.management.base import BaseCommand

from apps.landmatrix.models import Deal

from nanoid import generate


class Command(BaseCommand):
    def handle(self, *args, **options):
        for deal in Deal.objects.all().order_by("id"):
            print(deal.id)
            for x in deal.locations:
                if isinstance(x["id"], int):
                    x["id"] = generate(size=8)

            for x in deal.datasources:
                if isinstance(x["id"], int):
                    x["id"] = generate(size=8)

            for x in deal.contracts:
                if isinstance(x["id"], int):
                    x["id"] = generate(size=8)

            deal.save()

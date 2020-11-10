from django.core.management.base import BaseCommand

from apps.landmatrix.models import Deal


class Command(BaseCommand):
    def handle(self, *args, **options):
        deals = Deal.objects.all().order_by("id")
        for deal in deals:
            print(f"  Sync Deal {deal.id}... ", end="", flush=True)
            deal.save(custom_modification_date="-SKIP-")
            print("\033[92m" + "OK" + "\033[0m")

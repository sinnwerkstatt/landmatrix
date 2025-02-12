from django.core.management import BaseCommand

from apps.landmatrix.management.helpers import db_require_confirmation
from apps.landmatrix.models import schema
from apps.landmatrix.models.deal import DealVersion


class Command(BaseCommand):
    help = "Fix JSON array current flags."

    @db_require_confirmation
    def handle(self, *args, **options):
        # 547
        version = DealVersion.objects.get(id=85669)
        print(version)
        version.implementation_status = schema.CurrentDateChoiceImplementationStatus(
            set_current(version.implementation_status)
        )
        version.save()

        for v_id in [48727, 48728, 48729]:  # 688
            version = DealVersion.objects.get(id=v_id)
            print(version)
            version.negotiation_status = schema.CurrentDateChoiceNegotiationStatus(
                set_current(version.negotiation_status.model_dump())
            )
            version.save()

        for v_id in [67385, 67386]:  # 4393
            version = DealVersion.objects.get(id=v_id)
            print(version)
            version.contract_size = schema.CurrentDateAreaSchema(
                set_current(version.contract_size.model_dump())
            )
            version.save()

        for v_id in [81861, 81862]:  # 7978
            version = DealVersion.objects.get(id=v_id)
            print(version)
            version.negotiation_status = schema.CurrentDateChoiceNegotiationStatus(
                set_current(version.negotiation_status.model_dump())
            )
            version.save()

        for v_id in [82404, 82405]:  # 8111
            version = DealVersion.objects.get(id=v_id)
            print(version)
            version.production_size = schema.CurrentDateAreaSchema(
                set_current(version.production_size.model_dump())
            )
            version.save()

        print("DONE")


def set_current(array: list) -> list:
    return [*array[:-1], {**array[-1], "current": True}]

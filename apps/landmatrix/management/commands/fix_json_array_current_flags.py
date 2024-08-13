import re

from django.core.management import BaseCommand

from apps.landmatrix.models import schema
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

        # 547
        version = DealVersion.objects.get(id=85669)
        print(version)
        version.implementation_status = schema.CurrentDateChoiceImplementationStatus(
            set_current(version.implementation_status.model_dump())
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

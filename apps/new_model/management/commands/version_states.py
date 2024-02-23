from django.core.management.base import BaseCommand

from apps.landmatrix.models.deal import DealOld, DealVersion


class Command(BaseCommand):
    def handle(self, *args, **options):
        just_a_draft = []
        for deal in DealOld.objects.all().order_by("id"):  # type: DealOld
            print(deal.id)
            if deal.versions.count() == 1:
                dv: DealVersion = deal.versions.get()
                assert dv.serialized_data["status"] == 1
                assert dv.serialized_data["draft_status"] is not None
                just_a_draft += [deal.id]
            # print("other", deal.id)
        print(just_a_draft)

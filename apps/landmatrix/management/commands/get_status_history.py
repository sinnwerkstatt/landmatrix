from collections import Counter

from django.core.management.base import BaseCommand

from apps.landmatrix.models import HistoricalActivity, HistoricalInvestor


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Activities")
        acts = (
            HistoricalActivity.objects.all()
            # .filter(investor_identifier__lte=20)
            .order_by("activity_identifier", "id")
        )
        identifier = acts.first().activity_identifier
        status_set = []
        sets = []

        for act in acts:
            # print("ID: ",inv.investor_identifier, ", status: ", inv.fk_status_id)
            if act.activity_identifier == identifier:
                if len(status_set) > 1:
                    if not (
                        act.fk_status_id == status_set[-1]
                        and act.fk_status_id == status_set[-2]
                    ):
                        status_set += [act.fk_status_id]
                else:
                    status_set += [act.fk_status_id]
            else:
                identifier = act.activity_identifier
                sets += [tuple(status_set)]
                status_set = [act.fk_status_id]
            # print(status_set)
        ctr = sorted(Counter(sets).items(), key=lambda x: x[1])
        # print(ctr)
        for k, v in ctr:
            if k[-1] == 1:
                print("XX", k, v)
            else:
                print(k, v)
        # print(Counter(sets))

        print("Investors")
        invsts = (
            HistoricalInvestor.objects.all()
            # .filter(investor_identifier__lte=20)
            .order_by("investor_identifier", "id")
        )
        identifier = invsts.first().investor_identifier
        status_set = []
        sets = []

        for inv in invsts:
            # print("ID: ",inv.investor_identifier, ", status: ", inv.fk_status_id)
            if inv.investor_identifier == identifier:
                if len(status_set) > 1:
                    if not (
                        inv.fk_status_id == status_set[-1]
                        and inv.fk_status_id == status_set[-2]
                    ):
                        status_set += [inv.fk_status_id]
                else:
                    status_set += [inv.fk_status_id]
            else:
                identifier = inv.investor_identifier
                sets += [tuple(status_set)]
                status_set = [inv.fk_status_id]
            # print(status_set)
        ctr = sorted(Counter(sets).items(), key=lambda x: x[1])
        # print(ctr)
        for k, v in ctr:
            if k[-1] == 1:
                print("XX", k, v)
            else:
                print(k, v)
        # print(Counter(sets))

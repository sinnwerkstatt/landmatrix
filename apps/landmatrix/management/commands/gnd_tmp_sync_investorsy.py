from django.core.management.base import BaseCommand

from apps.landmatrix.models import Investor, HistoricalInvestorVentureInvolvement
from apps.landmatrix.synchronization.investor import histvestor_to_investor
from apps.landmatrix.models import HistoricalInvestor


def rec_resolve(histvestor, depth=0):
    prefix = depth * "\t"
    print(f"{prefix}Investor #{histvestor.investor_identifier}")
    for involve in HistoricalInvestorVentureInvolvement.objects.filter(
        fk_venture=histvestor
    ):
        try:
            Investor.objects.get(id=involve.fk_investor.investor_identifier)
        except Investor.DoesNotExist:
            print(
                f"{prefix}Having to go deeper: {involve.fk_investor}... ",
            )
            drueber = HistoricalInvestor.objects.filter(
                investor_identifier=involve.fk_investor.investor_identifier
            ).order_by("pk")
            for x in drueber:
                rec_resolve(x, depth + 1)
    histvestor_to_investor(histvestor)


alread_handled = set()


def rec_investor(investor_id, depth=0):
    if investor_id in alread_handled:
        return

    prefix = depth * "\t"
    print(f"{prefix}Investor #{investor_id}")
    for involve in HistoricalInvestorVentureInvolvement.objects.filter(
        fk_venture__investor_identifier=investor_id
    ):
        try:
            Investor.objects.get(id=involve.fk_investor.investor_identifier)
        except Investor.DoesNotExist:
            rec_investor(involve.fk_investor.investor_identifier, depth + 1)

    histvestor_versions = HistoricalInvestor.objects.filter(
        investor_identifier=investor_id
    ).order_by("pk")
    for histvestor in histvestor_versions:
        histvestor_to_investor(histvestor)
    alread_handled.add(investor_id)
    # print(histvestor_versions)


class Command(BaseCommand):
    def handle(self, *args, **options):
        all_investor_ids = (
            HistoricalInvestor.objects.values_list("investor_identifier", flat=True)
            .distinct()
            .order_by("investor_identifier")
        )

        for inv_id in all_investor_ids:
            rec_investor(inv_id)

        # print("Done.")
        # print("Lastly doing the rest - investors that have parents")
        # histvestor_versions = (
        #     HistoricalInvestor.objects.all()
        #     # .filter(investor_identifier__in=rest_list)
        #     .order_by("pk")
        # )
        # total = histvestor_versions.count()
        # i = 1
        # for histvestor in histvestor_versions:
        #     print(f"\r> {i}/{total} - ", end="")
        #     i += 1
        #     rec_resolve(histvestor, 0)

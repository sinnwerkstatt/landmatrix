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


class Command(BaseCommand):
    def handle(self, *args, **options):
        all_investor_ids = set(
            HistoricalInvestor.objects.values_list(
                "investor_identifier", flat=True
            ).distinct()
        )

        investings = set(
            HistoricalInvestorVentureInvolvement.objects.values_list(
                "fk_investor__investor_identifier", flat=True
            ).distinct()
        )
        ventures = set(
            HistoricalInvestorVentureInvolvement.objects.values_list(
                "fk_venture__investor_identifier", flat=True
            ).distinct()
        )

        print("Total number of investors", len(all_investor_ids))
        print("Investors that are parent companies only", len(investings))
        print("Investors that are being invested in", len(ventures))

        standalone = all_investor_ids - investings - ventures
        print("Investors that are standalone", len(standalone))
        # all_investor_ids
        okay_list = all_investor_ids - ventures
        rest_list = all_investor_ids - okay_list - standalone
        assert all_investor_ids == okay_list | rest_list
        assert ventures == rest_list
        print("rest list length", len(rest_list))

        # print((all_investor_ids - ventures - standalone) ^ investings)
        # assert investings == all_investor_ids - ventures - standalone
        # assert all_investor_ids == okay_list + standalone

        # print("Doing standalone investors first")
        # histvestor_versions = (
        #     HistoricalInvestor.objects.all()
        #     .filter(investor_identifier__in=standalone)
        #     .order_by("pk")
        # )
        # total = histvestor_versions.count()
        # i = 1
        # for histvestor in histvestor_versions:
        #     print(f"\r> {i}/{total}", end="")
        #     i += 1
        #     histvestor_to_investor(histvestor)
        #
        # print("done.")
        # print("Doing parent only next")
        # histvestor_versions = (
        #     HistoricalInvestor.objects.all()
        #     .filter(investor_identifier__in=okay_list)
        #     .order_by("pk")
        # )
        # total = histvestor_versions.count()
        # i = 1
        # for histvestor in histvestor_versions:
        #     print(f"\r> {i}/{total}", end="")
        #     i += 1
        #     histvestor_to_investor(histvestor)

        print("Done.")
        print("Lastly doing the rest - investors that have parents")
        histvestor_versions = (
            HistoricalInvestor.objects.all()
            # .filter(investor_identifier__in=rest_list)
            .order_by("pk")
        )
        total = histvestor_versions.count()
        i = 1
        for histvestor in histvestor_versions:
            print(f"\r> {i}/{total} - ", end="")
            i += 1
            rec_resolve(histvestor, 0)

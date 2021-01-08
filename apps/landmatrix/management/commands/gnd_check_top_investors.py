from collections import Counter

from django.core.management.base import BaseCommand

from apps.landmatrix.models import HistoricalActivity, HistoricalInvestor, Deal


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Activities")

        for deal in Deal.objects.all().order_by("id"):
            deal_investors = {i.id for i in deal.top_investors}

            ha = HistoricalActivity.objects.filter(activity_identifier=deal.id).first()
            ha_investors = {
                h.investor_identifier
                for h in ha.get_parent_companies(top_investors_only=True)
            }
            if not ha_investors == deal_investors:
                print(
                    f"{deal.id}: {deal_investors} ?= {ha_investors}: ",
                    ha_investors == deal_investors,
                )

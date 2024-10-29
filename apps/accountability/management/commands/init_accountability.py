from apps.landmatrix.models.deal import DealHull
from apps.accountability.models import DealScore, DealScoreVersion
from django.core.management import BaseCommand

from tqdm import tqdm


class Command(BaseCommand):
    def handle(self, *args, **options):
        qs_deals = DealHull.objects.filter(confidential=False).exclude(
            active_version__isnull=True
        )

        for deal in tqdm(qs_deals.iterator(), total=qs_deals.count()):
            #### SCRIPT TO DELETE STUFF
            # if DealScore.objects.filter(deal=deal).exists():
            #     DealScore.objects.filter(deal=deal).delete()

            #### SCRIPT TO ADD STUFF
            active_version = deal.active_version

            if active_version.status == "ACTIVATED":
                if not DealScore.objects.filter(deal=deal).exists():
                    deal_score = DealScore(deal=deal)
                    deal_score.save()

                    if not DealScoreVersion.objects.filter(
                        deal_version=active_version
                    ).exists():
                        deal_score_version = DealScoreVersion(
                            score=deal_score,
                            deal_version=active_version,
                        )
                        deal_score_version.save()

        print("DONE")

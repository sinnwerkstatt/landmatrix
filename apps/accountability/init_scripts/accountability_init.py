from apps.landmatrix.models.new import DealHull, DealVersion
from apps.accountability.models import DealScore, DealScoreVersion

print("########## EXECT INIT SCRIPT ##########")

all_deals = DealHull.objects.filter(confidential=False).exclude(active_version__isnull=True)

for deal in all_deals:
    #### SCRIPT TO DELETE STUFF
    # if DealScore.objects.filter(deal=deal).exists():
    #     DealScore.objects.filter(deal=deal).delete()

    #### SCRIPT TO ADD STUFF
    # Check if the active DealVersion already has attached DealScore
    active_version = deal.active_version

    if (active_version.status == "ACTIVATED"):
        # print(deal)
        if not DealScore.objects.filter(deal=deal).exists():
            deal_score = DealScore(deal=deal)
            deal_score.save()
        if not DealScoreVersion.objects.filter(deal_version=active_version).exists():
            deal_score_version = DealScoreVersion(score=deal_score, deal_version=active_version)
            deal_score_version.save()

print("DONE")
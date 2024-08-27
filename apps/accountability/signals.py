from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.landmatrix.models.new import DealHull, DealVersion
from apps.accountability.models import DealScore, DealScoreVersion

@receiver(post_save, sender=DealVersion)
def create_deal_score(sender, instance, **kwargs):
    # Only care for activated deals
    if (instance.status == "ACTIVATED"):
        if not DealScore.objects.filter(deal=instance.deal).exists():
            deal_score = DealScore(deal=instance.deal)
            deal_score.save()
        if not DealScoreVersion.objects.filter(deal_version=instance).exists():
            deal_score_version = DealScoreVersion(score=deal_score, deal_version=instance)
            deal_score_version.save()
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accountability.models import DealScore, DealScoreVersion
from apps.landmatrix.models.deal import DealHull, DealVersion


@receiver(post_save, sender=DealVersion)  # Actions when a new deal version is saved
def create_deal_score(sender, instance, **kwargs):
    # Only care for activated deals
    if instance.status == "ACTIVATED":
        deal_score, _ = DealScore.objects.get_or_create(deal=instance.deal)

        if not DealScoreVersion.objects.filter(deal_version=instance).exists():
            deal_score_version = DealScoreVersion(
                score=deal_score,
                deal_version=instance,
            )
            deal_score_version.save()

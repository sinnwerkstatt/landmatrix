from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models.investor import InvestorHull, Involvement


@receiver(post_save, sender=InvestorHull)
@receiver(post_delete, sender=InvestorHull)
def investor_updated(sender, instance: InvestorHull, **kwargs):
    for deal_version in instance.get_involved_deal_versions():
        deal_version.save(recalculate_independent=False)


@receiver(post_save, sender=Involvement)
@receiver(post_delete, sender=Involvement)
def involvement_updated(sender, instance: Involvement, **kwargs):
    for deal_version in instance.child_investor.get_involved_deal_versions():
        deal_version.save(recalculate_independent=False)

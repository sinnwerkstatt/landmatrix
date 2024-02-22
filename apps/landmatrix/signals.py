from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models.investor import Investor, InvestorVentureInvolvement


# TODO Nuts is this whole file still relevant?


@receiver(post_save, sender=Investor)
@receiver(post_delete, sender=Investor)
def investor_change_trigger_refresh_calculated_deal_fields(
    sender, instance: Investor, **kwargs
):
    for deal in instance.get_affected_deals():
        deal.save(recalculate_independent=False)


@receiver(post_save, sender=InvestorVentureInvolvement)
@receiver(post_delete, sender=InvestorVentureInvolvement)
def involvements_updated(sender, instance: InvestorVentureInvolvement, **kwargs):
    # Only consider the ventures deals. Because:
    # On an Involvement update the deals of the investor are not affected.
    for deal in instance.venture.get_affected_deals():
        deal.save(recalculate_independent=False)

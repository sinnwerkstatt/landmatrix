from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models.new import Involvement, InvestorHull, DealVersion


@receiver(post_save, sender=InvestorHull)
@receiver(post_delete, sender=InvestorHull)
def investor_change_trigger_refresh_calculated_deal_fields(
    sender, instance: InvestorHull, **kwargs
):
    dealversion: DealVersion
    for dealversion in instance.get_affected_deals():
        dealversion.save(recalculate_independent=False)


@receiver(post_save, sender=Involvement)
@receiver(post_delete, sender=Involvement)
def involvements_updated(sender, instance: Involvement, **kwargs):
    # Only consider the child_investors' deals. Because:
    # On an Involvement update the deals of the parent_investor are not affected.
    for deal in instance.child_investor.get_affected_deals():
        deal.save(recalculate_independent=False)

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models.new import Involvement, InvestorHull


# TODO nuts is this whole file still relevant? YES. do it.


@receiver(post_save, sender=InvestorHull)
@receiver(post_delete, sender=InvestorHull)
def investor_change_trigger_refresh_calculated_deal_fields(
    sender, instance: InvestorHull, **kwargs
):
    # TODO operating company blabla
    pass
    # for deal in instance.get_affected_deals():
    #     deal.save(recalculate_independent=False)


@receiver(post_save, sender=Involvement)
@receiver(post_delete, sender=Involvement)
def involvements_updated(sender, instance: Involvement, **kwargs):
    # Only consider the ventures deals. Because:
    # On an Involvement update the deals of the investor are not affected.
    pass
    # for deal in instance.venture.get_affected_deals():
    #     deal.save(recalculate_independent=False)

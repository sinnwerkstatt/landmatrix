from django.contrib.auth.models import Group
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete, m2m_changed, pre_delete
from django.dispatch import receiver
from django_registration.signals import user_registered

from apps.editor.models import UserRegionalInfo


# pylint: disable=unused-argument
from apps.landmatrix.models import (
    DataSource,
    Location,
    Contract,
    Investor,
    InvestorVentureInvolvement,
)


def create_userregionalinfo(sender, user, request, **kwargs):
    group, created = Group.objects.get_or_create(name="Reporters")
    user.groups.add(group)
    UserRegionalInfo.objects.create(
        user=user,
        phone=request.POST.get("phone", ""),
        information=request.POST.get("information", ""),
    )


user_registered.connect(create_userregionalinfo)


##### GREEN NEW DEAL SIGNALS ######
###################################


def invalidate_cache(sender, instance, **kwargs):
    # FIXME it is quite brute force to just empty the whole cache. fixme "some day"™️
    cache.clear()


post_save.connect(invalidate_cache)


@receiver(post_save, sender=Location)
@receiver(post_delete, sender=Location)
@receiver(post_save, sender=Contract)
@receiver(post_delete, sender=Contract)
@receiver(post_save, sender=DataSource)
@receiver(post_delete, sender=DataSource)
def deal_submodels_trigger_refresh_calculated_deal_fields(sender, instance, **kwargs):
    instance.deal.save(recalculate_independent=False)


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

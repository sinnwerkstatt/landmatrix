from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import tasks
from ..landmatrix import models


@receiver(post_save, sender=models.HistoricalActivity)
def signal_propagate_save_to_gnd_deal(sender, instance, **kwargs):
    if settings.CELERY_ENABLED:
        tasks.task_propagate_save_to_gnd_deal.delay(instance.pk)
    tasks.task_propagate_save_to_gnd_deal(instance.pk)


@receiver(post_save, sender=models.HistoricalInvestor)
def signal_propagate_save_to_gnd_investor(sender, instance, **kwargs):
    if settings.CELERY_ENABLED:
        tasks.task_propagate_save_to_gnd_investor.delay(instance.pk)
    tasks.task_propagate_save_to_gnd_investor(instance.pk)


@receiver(post_save, sender=models.HistoricalInvestorVentureInvolvement)
def signal_propagate_save_to_gnd_involvement(sender, instance, **kwargs):
    if settings.CELERY_ENABLED:
        tasks.task_propagate_save_to_gnd_involvement.delay(instance.pk)
    tasks.task_propagate_save_to_gnd_involvement(instance.pk)

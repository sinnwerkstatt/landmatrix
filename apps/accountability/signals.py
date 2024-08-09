from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.landmatrix.models.new import DealHull
from apps.accountability.models import DealScore

# @receiver(pre_save, sender=DealHull)
# def deal_save(sender, **kwargs):
#     if sender.pk is None:

from django.db.models.signals import post_save
from django.dispatch import receiver

from landmatrix.models import HistoricalActivity
from landmatrix.tasks import index_activity

@receiver(post_save, sender=HistoricalActivity)
def index_document(sender, instance, **kwargs):
    index_activity.delay(instance.id)
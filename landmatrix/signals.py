from django.db.models.signals import post_save
from django.dispatch import receiver

from api.elasticsearch import es_save
from landmatrix.models import HistoricalActivity

@receiver(post_save, sender=HistoricalActivity)
def index_document(sender, instance, **kwargs):
    es_save.index_document(instance)
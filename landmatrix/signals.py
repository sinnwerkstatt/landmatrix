from django.db.models.signals import post_save
from django.dispatch import receiver

from api.elasticsearch import ElasticSearch
from landmatrix.models import HistoricalActivity

@receiver(post_save, sender=HistoricalActivity)
def index_document(sender, instance, **kwargs):
    es = ElasticSearch()
    es.index_document(instance)
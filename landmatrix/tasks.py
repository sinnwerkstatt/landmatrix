from __future__ import absolute_import

from celery import shared_task
from api.elasticsearch import es_save

@shared_task
def index_activity(activity):
    #es_save.index_document(activity)
    pass
from __future__ import absolute_import

from celery import shared_task
from api.elasticsearch import es_save

@shared_task
def index_activity(activity_id):
    es_save.index_document_by_id(activity_id=activity_id)
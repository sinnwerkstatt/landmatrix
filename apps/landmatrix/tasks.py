# pylint: disable=unused-argument
import time

from celery import shared_task
from django.conf import settings

from apps.api.elasticsearch import es_save
from apps.landmatrix.celery_app import app
from apps.landmatrix.synchronization.deal import histivity_to_deal
from apps.landmatrix.synchronization.investor import histvestor_to_investor


# ### Green New Deal ### #
@shared_task
def task_propagate_save_to_gnd_deal(hist_deal_pk):
    histivity_to_deal(activity_pk=hist_deal_pk)


@shared_task
def task_propagate_save_to_gnd_investor(histvestor_id):
    histvestor_to_investor(histvestor_id)


# ### Green New Deal ### #


@app.task(name="%s.tasks.index_activity" % settings.CELERY_NAME, bind=True)
def index_activity(self, activity_identifier):
    es_save.delete_historicalactivity(activity_identifier=activity_identifier)
    # For some reason without sleep indexing happens before deleting
    time.sleep(5)
    es_save.index_activity(activity_identifier=activity_identifier)


@app.task(name="%s.tasks.delete_historicalactivity" % settings.CELERY_NAME, bind=True)
def delete_historicalactivity(self, activity_identifier):
    es_save.delete_historicalactivity(activity_identifier=activity_identifier)


@app.task(name="%s.tasks.index_investor" % settings.CELERY_NAME, bind=True)
def index_investor(self, investor_identifier):
    es_save.delete_historicalinvestor(investor_identifier=investor_identifier)
    # For some reason without sleep indexing happens before deleting
    time.sleep(5)
    es_save.index_investor(investor_identifier=investor_identifier)


@app.task(name="%s.tasks.delete_historicalinvestor" % settings.CELERY_NAME, bind=True)
def delete_historicalinvestor(self, investor_identifier):
    es_save.delete_historicalinvestor(investor_identifier=investor_identifier)

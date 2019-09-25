from __future__ import absolute_import

import time

from django.conf import settings

from apps.api.elasticsearch import es_save
from apps.landmatrix.celery_app import app


@app.task(name="%s.tasks.index_activity" % settings.CELERY_NAME, bind=True)
def index_activity(self, activity_identifier):
    es_save.delete_activity(activity_identifier=activity_identifier)
    # For some reason without sleep indexing happens before deleting
    time.sleep(5)
    es_save.index_activity(activity_identifier=activity_identifier)


@app.task(name="%s.tasks.delete_activity" % settings.CELERY_NAME, bind=True)
def delete_activity(self, activity_identifier):
    es_save.delete_activity(activity_identifier=activity_identifier)


@app.task(name="%s.tasks.index_investor" % settings.CELERY_NAME, bind=True)
def index_investor(self, investor_identifier):
    es_save.delete_investor(investor_identifier=investor_identifier)
    # For some reason without sleep indexing happens before deleting
    time.sleep(5)
    es_save.index_investor(investor_identifier=investor_identifier)


@app.task(name="%s.tasks.delete_investor" % settings.CELERY_NAME, bind=True)
def delete_investor(self, investor_identifier):
    es_save.delete_investor(investor_identifier=investor_identifier)

from __future__ import absolute_import

from django.conf import settings

from landmatrix.celery import app
from api.elasticsearch import es_save


@app.task(name='%s.tasks.index_activity' % settings.CELERY_NAME, bind=True)
def index_activity(self, activity_id):
    es_save.index_activity_by_id(activity_id=activity_id)


@app.task(name='%s.tasks.delete_activity' % settings.CELERY_NAME, bind=True)
def delete_activity(self, activity_identifier):
    es_save.delete_activity(activity_identifier=activity_identifier)


@app.task(name='%s.tasks.index_investor' % settings.CELERY_NAME, bind=True)
def index_investor(self, activity_id):
    es_save.index_investor_by_id(activity_id=activity_id)


@app.task(name='%s.tasks.delete_investor' % settings.CELERY_NAME, bind=True)
def delete_investor(self, investor_identifier):
    es_save.delete_investor(investor_identifier=investor_identifier)


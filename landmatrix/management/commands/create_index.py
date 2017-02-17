#!/usr/bin/env python
import os
import sys
from pyelasticsearch import ElasticSearch, BulkError
from pyelasticsearch.exceptions import ElasticHttpNotFoundError, ElasticHttpError

from django.core.management import BaseCommand

from landmatrix.models.activity import Activity
from grid.views.change_deal_view import ChangeDealView

FIELD_TYPE_MAPPING = {
    'IntegerField': 'integer',
    'CharField': 'string',
}

class Command(BaseCommand):
    help = 'Index deals for elasticsearch'
    es = None

    def handle(self, *args, **options):
        self.es = ElasticSearch('http://localhost:9200/')
        self.create_index()
        self.index_documents()
        self.refresh_index()
        #self.stdout.write('Indexed %i deals' % len(activities))

    def get_properties(self):
        # Get field type mappings
        properties = {}
        for form in ChangeDealView.FORMS:
            form = hasattr(form, "form") and form.form or form
            for name, field in form.base_fields.items():
                # Title field?
                if name.startswith('tg_') and not name.endswith('_comment'):
                    continue
                properties[name] = FIELD_TYPE_MAPPING.get(field.__class__.__name__, 'string')
        return properties

    def create_index(self, delete=True):
        if delete:
            try:
                self.es.delete_index('landmatrix')
            except ElasticHttpNotFoundError as e:
                raise 
        # Create index
        deal_mapping = {
            'deal': {
                'properties': self.get_properties()
            }
        }
        try:
            self.es.create_index('landmatrix', settings={'mappings': deal_mapping})
        except ElasticHttpError as e:
            pass

    def index_documents(self):
        # Index documents
        docs = []
        activities = Activity.objects.all()
        for activity in activities:
            deal = {'id': activity.activity_identifier}
            deal.update(dict([a.name, a.value] for a in activity.attributes.all()))
            docs.append(deal)
        try:
            self.es.bulk((self.es.index_op(doc, id=doc.pop('id')) for doc in docs),
                index='landmatrix',
                doc_type='deal')
        except BulkError as e:
            for err in e.errors:
                self.stderr.write('%s: %s (ID: %s)' % (
                    err['index']['error']['reason'],
                    err['index']['error']['caused_by']['reason'],
                    err['index']['_id']
                ))

    def refresh_index(self):
        # Refresh index
        self.es.refresh('landmatrix')
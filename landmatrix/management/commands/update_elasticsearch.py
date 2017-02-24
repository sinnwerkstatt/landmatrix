#!/usr/bin/env python
import os
import sys

from django.core.management import BaseCommand
from pyelasticsearch import BulkError

from landmatrix.models.activity import HistoricalActivity
from api.elasticsearch import es_save


class Command(BaseCommand):
    help = 'Update deal index for elasticsearch'
    es = None

    def handle(self, *args, **options):
        es = es_save
        try:
            es.index_documents_by_version(drop_index=True)
        except BulkError as e:
            for err in e.errors:
                self.stderr.write('%s: %s (ID: %s)' % (
                    err['index']['error']['reason'],
                    err['index']['error']['caused_by']['reason'],
                    err['index']['_id']
                ))
        es.refresh_index()

        #self.stdout.write(str(self.es.get_mapping('landmatrix')))
        #self.stdout.write('Indexed %i deals' % len(activities))
        
#!/usr/bin/env python
import os
import sys

from django.core.management import BaseCommand

from api.elasticsearch import es_save


class Command(BaseCommand):
    help = 'Update deal index for elasticsearch'
    es = None

    def handle(self, *args, **options):
        es = es_save
        es.create_index(delete=True)
        es.stdout = self.stdout
        es.stderr = self.stderr
        es.index_activity_documents()
        es.index_investor_documents()
        es.refresh_index()

        #self.stdout.write(str(self.es.get_mapping('landmatrix')))
        #self.stdout.write('Indexed %i deals' % len(activities))
        
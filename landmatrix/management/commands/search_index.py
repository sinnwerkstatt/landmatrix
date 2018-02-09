#!/usr/bin/env python

from django.core.management import BaseCommand

from api.elasticsearch import es_save, DOC_TYPES_ACTIVITY, DOC_TYPES_INVESTOR


class Command(BaseCommand):
    help = 'Update deal index for elasticsearch'
    es = None

    def add_arguments(self, parser):
        parser.add_argument(
            '-rb', '--rebuild', action='store_true', dest='rebuild',
            help="Rebuild index",
        )
        parser.add_argument(
            '-d', '--delete', action='store_true', dest='delete',
            help="Delete index",
        )
        parser.add_argument(
            '-rf', '--refresh', action='store_true', dest='refresh',
            help="Refresh index",
        )
        parser.add_argument(
            '-dt', '--doc-type', type=str, dest='doc_type',
            help="Doc type",
        )

    def handle(self, *args, **options):
        rebuild = options.get('rebuild')
        delete = options.get('delete')
        refresh = options.get('refresh')
        doc_type = options.get('doc_type')

        es = es_save
        es.stdout = self.stdout
        es.stderr = self.stderr

        if delete or (rebuild and not doc_type):
            es.create_index(delete=True)

        if rebuild:
            if doc_type:
                if doc_type in DOC_TYPES_ACTIVITY:
                    es.index_activity_documents(doc_types=[doc_type,])
                elif doc_type in DOC_TYPES_INVESTOR:
                    es.index_investor_documents(doc_types=[doc_type,])
            else:
                es.index_activity_documents()
                es.index_investor_documents()

        if rebuild or refresh:
            es.refresh_index()

#!/usr/bin/env python
from django.core.management import BaseCommand
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser

from openpyxl import load_workbook

from grid.views.export_view import ExportView
from grid.views.all_deals_view import AllDealsView


class Command(BaseCommand):
    help = 'Check if export number of deals is same as grid.' \
           'Return list of differing deals.'

    def handle(self, *args, **options):
        # Get export
        rf = RequestFactory()
        request = rf.get('/data/all.xls')
        request.session = {}
        request.user = AnonymousUser()
        export = ExportView()
        export.request = request
        export.set_default_filters({})
        query = export.create_query_from_filters()
        sort = ['activity_identifier',]
        results = {}
        deals = export.execute_elasticsearch_query(query, doc_type='deal', fallback=False,
                                                  sort=sort)
        deals = export.filter_returned_results(deals)
        deals = export.merge_deals(deals)
        export_deals = list(deals)
        export_ids = set(row['activity_identifier'] for row in export_deals)
        export_count = len(export_ids)

        # Get grid
        rf = RequestFactory()
        request = rf.get('/data/')
        request.session = {}
        request.user = AnonymousUser()
        grid = AllDealsView()
        grid.group = 'all'
        grid.request = request
        grid._limit_query = lambda: False
        query_result = grid.get_records()
        grid_deals = grid._get_items(query_result)
        grid_ids = set(row['deal_id'] for row in grid_deals)
        grid_count = len(grid_ids)

        self.stdout.write("{} deals found in export".format(str(export_count)))
        self.stdout.write("{} deals found in grid".format(str(grid_count)))

        missing_grid = export_ids - grid_ids
        self.stdout.write("{} deals missing in grid ({})".format(str(len(missing_grid)),
                                                                 ', '.join([str(i)
                                                                            for i in
                                                                            missing_grid])))
        missing_export = grid_ids - export_ids
        self.stdout.write("{} deals missing in export ({})".format(str(len(missing_export)),
                                                                 ', '.join([str(i) for i in
                                                                            missing_export])))
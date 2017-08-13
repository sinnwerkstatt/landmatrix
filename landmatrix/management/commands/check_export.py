#!/usr/bin/env python
import os
import sys
import csv
from collections import OrderedDict
from django.core.management import BaseCommand
from django.db import connections
from openpyxl import load_workbook


EMPTY_ALLOWED = (
    'Location 1: Facility name',
    'Location 1: Location description',
    'Location 1: Contract area',
    'Location 1: Intended area',
    'Location 1: Area in operation',
    'Location 2: Facility name',
    'Location 2: Location description',
    'Location 2: Contract area',
    'Location 2: Intended area',
    'Location 2: Area in operation',
    'Location 3: Facility name',
    'Location 3: Location description',
    'Location 3: Contract area',
    'Location 3: Intended area',
    'Location 3: Area in operation',
    'Location 4: Facility name',
    'Location 4: Location description',
    'Location 4: Contract area',
    'Location 4: Intended area',
    'Location 4: Area in operation',
    'Location 5: Facility name',
    'Location 5: Location description',
    'Location 5: Contract area',
    'Location 5: Intended area',
    'Location 5: Area in operation',
    'Location 6: Facility name',
    'Location 6: Location description',
    'Location 6: Contract area',
    'Location 6: Intended area',
    'Location 6: Area in operation',
    'Location 7: Facility name',
    'Location 7: Location description',
    'Location 7: Contract area',
    'Location 7: Intended area',
    'Location 7: Area in operation',
    'Location 8: Facility name',
    'Location 8: Location description',
    'Location 8: Contract area',
    'Location 8: Intended area',
    'Location 8: Area in operation',
    'Location 9: Facility name',
    'Location 9: Location description',
    'Location 9: Contract area',
    'Location 9: Intended area',
    'Location 9: Area in operation',
    'On leased / purchased households',
    'Not on leased / purchased households (out-grower)',
    'Contracts 1: Contract expiration date',
    'Contracts 1: Sold as deal no.',
    'Contracts 1: Comment on Contract',
    'Planned daily/seasonal workers (foreign)',
    'Current number of daily/seasonal workers (foreign)',
    'Actors involved in the negotiation / admission process',
    'Operational company: Parent relation',
    'Operational company: Investor homepage',
    'Operational company: Opencorporates link',
    'Operational company: Comment',
    'Operational company: Subinvestors',
    'Data source 1: Keep PDF not public',
    'Data source 1: Publication title',
    'Data source 1: OpenLandContracts ID',
    'Data source 2: Keep PDF not public',
    'Data source 2: Publication title',
    'Data source 2: OpenLandContracts ID',
    'Data source 3: Keep PDF not public',
    'Data source 3: Publication title',
    'Data source 3: OpenLandContracts ID',
    'Data source 4: Keep PDF not public',
    'Data source 4: Publication title',
    'Data source 4: OpenLandContracts ID',
    'Data source 5: Keep PDF not public',
    'Data source 5: Publication title',
    'Data source 5: OpenLandContracts ID',
    'Data source 6: Keep PDF not public',
    'Data source 6: Publication title',
    'Data source 6: OpenLandContracts ID',
    'Data source 7: Keep PDF not public',
    'Data source 7: Publication title',
    'Data source 7: OpenLandContracts ID',
    'Data source 8: Keep PDF not public',
    'Data source 8: Publication title',
    'Data source 8: OpenLandContracts ID',
    'Data source 9: Keep PDF not public',
    'Data source 9: Publication title',
    'Data source 9: Phone',
    'Data source 9: OpenLandContracts ID',
    'Name of community',
    'Name of indigenous people',
    'Comment on Names of affected people',
    'Recognition status of community land tenure',
    'Comment on Recognitions status of community land tenure',
    'Presence of land conflicts',
    'Comment on Presence of land conflicts',
    'Displacement of people',
    'Number of households actually displaced',
    'Number of people displaced out of their community land',
    'Number of people displaced staying on community land',
    'Number of households displaced "only" from their agricultural fields',
    'Number of people facing displacement once project is fully implemented',
    'Negative impacts for local communities',
    'Comment on Negative impacts for local communities',
    'Received compensation (e.g. for damages or resettlements)',
    'Comment on Promised benefits for local communities',
    'Materialized benefits for local communities',
    'Comment on Materialized benefits for local communities',
    'Presence of organizations and actions taken (e.g. farmer organizations, NGOs, etc.)',
    'Crops yield',
    'Crops export',
    'Comment on Crops',
    'Livestock yield',
    'Livestock export',
    'Comment on Livestock',
    'Resources yield',
    'Resources export',
    'Comment on Resources',
    'Contract farming crops',
    'Comment on Contract farming crops',
    'Contract farming livestock',
    'Comment on Contract farming livestock',
    'Country 1',
    'Country 2',
    'Country 3',
    'Country 3 ratio',
    'Processing facilities / production infrastructure of the project (e.g. oil mill, ethanol distillery, biomass power plant etc.)',
    'In-country end products of the project',
    'Use of irrigation infrastructure',
    'Comment on Use of irrigation infrastructure',
    'Water footprint of the investment project',
    'Application of Voluntary Guidelines on the Responsible Governance of Tenure (VGGT)',
    'Comment on VGGT',
    'Application of Principles for Responsible Agricultural Investments (PRAI)',
    'Comment on PRAI',
)
NO_EMPTY_ALLOWED = (
    'Deal ID',
    'Is public',
    'Deal scope',
    'Deal size',
    'Top parent companies',
    'Location 1: Latitude',
    'Location 1: Longitude',
    'Location 1: Target Country',
    'Operational company: Investor ID',
    'Negotiation status',
)

class Command(BaseCommand):
    help = 'Check if export has any errors (for internal QA)'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        wb = load_workbook(filename=options['file'][0], read_only=True)
        ## Check row count
        ws = wb['Deals']
        if len(list(ws.rows)) < 2:
            self.stderr.write('No data in Sheet Deals')
        ws = wb['Involvements']
        if len(list(ws.rows)) < 2:
            self.stderr.write('No data in Sheet Involvements')
        ws = wb['Investors']
        if len(list(ws.rows)) < 2:
            self.stderr.write('No data in Sheet Investors')

        ## Check top parent companies
        # Get columns and investors
        columns = []
        investors = {}
        ws = wb['Investors']
        for i, row in enumerate(ws.rows):
            if i == 0:
                continue
            id = row[0].value
            if id in investors.keys():
                self.stderr.write('Duplicate investor ID: %s (Sheet: Investors)' % id)
            investors[id] = [cell.value for cell in row]

        ws = wb['Deals']
        for i, row in enumerate(ws.rows):
            if i == 0:
                continue
            if not row[5].value:
                continue
            top_investors = row[5].value.split('|')
            for investor in top_investors:
                if not investor:
                    continue
                id, name = investor.split('#')
                if not id in investors.keys():
                    self.stderr.write('Missing investor ID: %s (Sheet: Deals)' % id)

        ## Check for empty columns or columns with empty fields
        for i, row in enumerate(ws.rows):
            if i == 0:
                for column in row:
                    columns.append({
                        'label': column.value,
                        'items': []
                    })
                continue
            for j, cell in enumerate(row):
                columns[j]['items'].append(str(cell.value or '').strip())
        rows = len(list(ws.rows))
        for column in columns:
            count = len(list(filter(None, column['items'])))
            if count == 0 and column['label'] not in EMPTY_ALLOWED:
                self.stderr.write('No values in column "%s" (Sheet: Deals)' % column['label'])

            count = len(list(filter(None, column['items'])))
            if column['label'] in NO_EMPTY_ALLOWED and count < rows:
                self.stderr.write('%i missing values in column "%s" (Sheet: Deals)' % (
                    rows - count,
                    column['label'],
                ))

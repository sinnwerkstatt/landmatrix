#!/usr/bin/env python
import os
import sys
import csv
from collections import OrderedDict
from django.core.management import BaseCommand
from django.db import connections
from openpyxl import load_workbook


class Command(BaseCommand):
    help = 'Check if export has any errors (for internal QA)'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        wb = load_workbook(filename=options['file'][0], read_only=True)
        ## Check top parent companies
        # Get investors
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
            top_investors = row[5].value.split('|')
            for investor in top_investors:
                if not investor:
                    continue
                print(investor)
                id, name = investor.split('#')
                if not id in investors.keys():
                    self.stderr.write('Missing investor ID: %s (Sheet: Investors)' % id)
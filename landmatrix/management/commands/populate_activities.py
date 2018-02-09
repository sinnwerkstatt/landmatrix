#!/usr/bin/env python
import os
import sys
from django.core.management import BaseCommand

from landmatrix.models.activity import Activity


class Command(BaseCommand):
    help = 'Populates the activities with common used attributes'

    def handle(self, *args, **options):
        count = Activity.objects.count()
        for i, a in enumerate(Activity.objects.all()):
            self.stdout.write('Activity %i/%i' % (i, count), ending='\r')
            self.stdout.flush()
            a.refresh_cached_attributes()

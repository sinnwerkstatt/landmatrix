#!/usr/bin/env python
import os
import sys
from django.core.management import BaseCommand

from landmatrix.models.activity import Activity
from grid.views.activity_protocol import ActivityProtocol


class Command(BaseCommand):
    help = 'Populates the activities with common used attributes'

    def handle(self, *args, **options):
        for a in Activity.objects.all():
            a.refresh_cached_attributes()

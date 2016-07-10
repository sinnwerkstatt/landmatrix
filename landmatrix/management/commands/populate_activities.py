#!/usr/bin/env python
import os
import sys
from django.core.management import BaseCommand

from grid.views.activity_protocol import ActivityProtocol

class Command(BaseCommand):
    help = 'Populates the activities with common used attributes'

    def handle(self, *args, **options):
        from landmatrix.models import Activity

        activities = Activity.objects.all().values_list('activity_identifier', flat=True)
        ap = ActivityProtocol()
        for activity_identifier in activities:
            ap.prepare_deal_for_public_interface(activity_identifier)

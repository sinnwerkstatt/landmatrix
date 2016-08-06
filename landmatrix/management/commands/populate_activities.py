#!/usr/bin/env python
import os
import sys
from django.core.management import BaseCommand

from landmatrix.models.activity import Activity, ActivityProtocol

class Command(BaseCommand):
    help = 'Populates the activities with common used attributes'

    def handle(self, *args, **options):
        activities = Activity.objects.all().values_list('activity_identifier', flat=True)
        ap = ActivityProtocol()
        for activity_identifier in activities:
            ap.prepare_deal_for_public_interface(activity_identifier)

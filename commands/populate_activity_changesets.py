#!/usr/bin/env python
import os
import sys
from django.core.management import BaseCommand

from apps.landmatrix.models.activity_changeset import ActivityChangeset


class Command(BaseCommand):
    help = "Populates the activity changesets with countries"

    def handle(self, *args, **options):
        count = ActivityChangeset.objects.count()
        for i, c in enumerate(ActivityChangeset.objects.all()):
            self.stdout.write("Activity Changeset %i/%i" % (i, count), ending="\r")
            self.stdout.flush()
            if c.fk_activity:
                c.fk_country = c.fk_activity.target_country
                c.save()

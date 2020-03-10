#!/usr/bin/env python
from django.core.management import BaseCommand

from apps.landmatrix.models import HistoricalActivity


class Command(BaseCommand):
    help = "Checks why deal is not public"

    def add_arguments(self, parser):
        parser.add_argument("activity_identifier", nargs="+", type=str)

    def handle(self, *args, **options):
        activity = HistoricalActivity.objects.get(
            activity_identifier=options["activity_identifier"][0]
        )
        self.stdout.write(activity.get_not_public_reason())

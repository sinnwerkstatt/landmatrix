#!/usr/bin/env python
import re

from django.core.management import BaseCommand

from apps.landmatrix.models import HistoricalActivity, ActivityAttributeGroup


class Command(BaseCommand):
    help = "Clean names of Activity attribute groups (previously known as Tag groups)."

    def handle(self, *args, **options):
        activities = HistoricalActivity.objects.all()
        count = activities.count()
        for i, activity in enumerate(activities):
            self.stdout.write("HistoricalActivity %i/%i" % (i, count), ending="\r")
            self.stdout.flush()
            for j, attribute in enumerate(
                activity.attributes.order_by("fk_group__name")
            ):
                old_name = attribute.fk_group.name
                match = re.match("(.*?)_(\d+)", old_name)
                if match:
                    new_name = "%s_%02i" % (match.groups()[0], j + 1)
                    try:
                        group, created = ActivityAttributeGroup.objects.get_or_create(
                            name=new_name
                        )
                        attribute.fk_group = group
                        attribute.save()
                    except:
                        print(new_name)
                        raise

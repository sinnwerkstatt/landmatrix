#!/usr/bin/env python
import re

from django.core.management import BaseCommand

from landmatrix.models import *


class Command(BaseCommand):
    help = 'Clean names of Activity attribute groups'

    def handle(self, *args, **options):
        activities = Activity.objects.all()
        count = activities.count()
        for i, activity in enumerate(activities):
            self.stdout.write('Activity %i/%i' % (i, count), ending='\r')
            self.stdout.flush()
            group_count = 0
            for group_name in activity.attributes.order_by('fk_group__name').values('fk_group__name'):
                group_name = group_name['fk_group__name']
                match = re.match('(.*?)_(\d)', group_name)
                if not match:
                    continue
                group_count += 1
                new_name = '%s_%02i' % (
                    match.groups()[0],
                    group_count
                )
                group, created = ActivityAttributeGroup.objects.get_or_create(name=new_name)
                for attribute in activity.attributes.filter(fk_group__name=group_name):
                    attribute.fk_group = group
                    attribute.save()

        activities = HistoricalActivity.objects.all()
        count = activities.count()
        for i, activity in enumerate(activities):
            self.stdout.write('HistoricalActivity %i/%i' % (i, count), ending='\r')
            self.stdout.flush()
            for j, attribute in enumerate(activity.attributes.order_by('fk_group__name')):
                old_name = attribute.fk_group.name
                match = re.match('(.*?)_(\d)', old_name)
                if match:
                    new_name = '%s_%02i' % (
                        match.groups()[0],
                        j + 1
                    )
                    try:
                        group, created = ActivityAttributeGroup.objects.get_or_create(name=new_name)
                        attribute.fk_group = group
                        attribute.save()
                    except:
                        print(new_name)
                        raise
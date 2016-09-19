# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def populate_activity_rel(apps, schema_editor):
    Activity = apps.get_model('landmatrix', 'Activity')
    HistoricalActivity = apps.get_model('landmatrix', 'HistoricalActivity')

    for activity in Activity.objects.all():
        try:
            historical_activity = HistoricalActivity.objects.get(
                pk=activity.pk,
                activity_identifier=activity.activity_identifier)
        except HistoricalActivity.DoesNotExist:
            pass
        else:
            historical_activity.public_version = activity
            historical_activity.save(update_fields=['public_version'])


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0091_add_activity_rel'),
    ]

    operations = [
        migrations.RunPython(populate_activity_rel),
    ]

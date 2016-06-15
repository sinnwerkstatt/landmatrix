# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0072_auto_20160615_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityattribute',
            name='value2',
            field=models.TextField(max_length=255, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalactivityattribute',
            name='value2',
            field=models.TextField(max_length=255, blank=True, null=True),
        ),
    ]

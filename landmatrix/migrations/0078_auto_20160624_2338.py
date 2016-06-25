# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0077_auto_20160619_2120'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='investoractivityinvolvement',
            options={'ordering': ('-timestamp',), 'verbose_name': 'Investor Activity Involvements', 'get_latest_by': 'timestamp'},
        ),
        migrations.AlterField(
            model_name='activitychangeset',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Timestamp'),
        ),
        migrations.AlterField(
            model_name='filtercondition',
            name='value',
            field=models.CharField(max_length=1024, verbose_name='Value', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalactivity',
            name='history_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

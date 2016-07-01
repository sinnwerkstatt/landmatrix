# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0083_auto_20160627_0132'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'permissions': (('review_activity', 'Can review activity changes'),), 'verbose_name': 'Activity', 'verbose_name_plural': 'Activities'},
        ),
        migrations.RemoveField(
            model_name='activity',
            name='fully_updated_old',
        ),
        migrations.RemoveField(
            model_name='activitychangeset',
            name='fk_region',
        ),
        migrations.RemoveField(
            model_name='historicalactivity',
            name='fully_updated_old',
        ),
        migrations.AlterField(
            model_name='activitychangeset',
            name='fk_activity',
            field=models.ForeignKey(related_name='changesets', to='landmatrix.HistoricalActivity', blank=True, null=True, verbose_name='Activity'),
        ),
        migrations.AlterField(
            model_name='activitychangeset',
            name='timestamp',
            field=models.DateTimeField(blank=True, verbose_name='Timestamp', null=True),
        ),
    ]

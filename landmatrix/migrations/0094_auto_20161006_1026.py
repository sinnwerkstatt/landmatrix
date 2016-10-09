# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0093_auto_20160930_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityattribute',
            name='is_current',
            field=models.BooleanField(verbose_name='Is current', default=False),
        ),
        migrations.AddField(
            model_name='historicalactivityattribute',
            name='is_current',
            field=models.BooleanField(verbose_name='Is current', default=False),
        ),
        migrations.AlterField(
            model_name='investorventureinvolvement',
            name='investment_type',
            field=models.CommaSeparatedIntegerField(blank=True, null=True, default='', choices=[(10, 'Shares/Equity'), (20, 'Debt financing')], max_length=255),
        ),
    ]

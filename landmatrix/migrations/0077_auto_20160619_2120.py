# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0076_auto_20160619_1515'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalinvestor',
            options={'verbose_name_plural': 'Historical investors', 'get_latest_by': 'history_date', 'verbose_name': 'Historical investor', 'ordering': ['-history_date']},
        ),
        migrations.AlterField(
            model_name='activitychangeset',
            name='fk_activity',
            field=models.ForeignKey(null=True, to='landmatrix.HistoricalActivity', verbose_name='Activity', blank=True),
        ),
        migrations.AlterField(
            model_name='investorventureinvolvement',
            name='loans_currency',
            field=models.ForeignKey(null=True, to='landmatrix.Currency', verbose_name='Loan currency', blank=True),
        ),
    ]

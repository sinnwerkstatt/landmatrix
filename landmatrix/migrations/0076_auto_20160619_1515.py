# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0075_auto_20160618_1721'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalactivity',
            options={'verbose_name': 'Historical activity', 'verbose_name_plural': 'Historical activities', 'ordering': ('-history_date',), 'get_latest_by': 'history_date'},
        ),
        migrations.AlterModelOptions(
            name='historicalactivityattribute',
            options={'verbose_name': 'Historical activity attribute', 'verbose_name_plural': 'Historical activity attributes', 'get_latest_by': 'history_date'},
        ),
        migrations.AddField(
            model_name='historicalinvestor',
            name='parent_relation',
            field=models.CharField(null=True, blank=True, choices=[('Subsidiary', 'Subsidiary of parent company'), ('Local branch', 'Local branch of parent company'), ('Joint venture', 'Joint venture of parent companies')], max_length=255),
        ),
        migrations.AddField(
            model_name='investor',
            name='parent_relation',
            field=models.CharField(null=True, blank=True, choices=[('Subsidiary', 'Subsidiary of parent company'), ('Local branch', 'Local branch of parent company'), ('Joint venture', 'Joint venture of parent companies')], max_length=255),
        ),
        migrations.AlterField(
            model_name='activity',
            name='fully_updated',
            field=models.DateTimeField(null=True, blank=True, verbose_name='Fully updated'),
        ),
        migrations.AlterField(
            model_name='activitychangeset',
            name='timestamp',
            field=models.DateTimeField(verbose_name='Timestamp'),
        ),
        migrations.AlterField(
            model_name='historicalactivity',
            name='fully_updated',
            field=models.DateTimeField(null=True, blank=True, verbose_name='Fully updated'),
        ),
        migrations.AlterField(
            model_name='historicalactivity',
            name='history_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='historicalactivityattribute',
            name='fk_activity',
            field=models.ForeignKey(to='landmatrix.HistoricalActivity', related_name='attributes', verbose_name='Activity'),
        ),
        migrations.AlterField(
            model_name='historicalinvestor',
            name='classification',
            field=models.CharField(null=True, blank=True, choices=[('10', 'Private company'), ('20', 'Stock-exchange listed company'), ('30', 'Individual entrepreneur'), ('40', 'Investment fund'), ('50', 'Semi state-owned company'), ('60', 'State-/government (owned) company'), ('70', 'Other (please specify in comment field)'), ('110', 'Government'), ('120', 'Government institution'), ('130', 'Multilateral Development Bank (MDB)'), ('140', 'Bilateral Development Bank / Development Finance Institution'), ('150', 'Commercial Bank'), ('160', 'Investment Bank'), ('170', 'Investment Fund (all types incl. pension, hedge, mutual, private equity funds etc.)'), ('180', 'Insurance firm'), ('190', 'Private equity firm'), ('200', 'Asset management firm'), ('210', 'Non - Profit organization (e.g. Church, University etc.)')], max_length=3),
        ),
        migrations.AlterField(
            model_name='investor',
            name='classification',
            field=models.CharField(null=True, blank=True, choices=[('10', 'Private company'), ('20', 'Stock-exchange listed company'), ('30', 'Individual entrepreneur'), ('40', 'Investment fund'), ('50', 'Semi state-owned company'), ('60', 'State-/government (owned) company'), ('70', 'Other (please specify in comment field)'), ('110', 'Government'), ('120', 'Government institution'), ('130', 'Multilateral Development Bank (MDB)'), ('140', 'Bilateral Development Bank / Development Finance Institution'), ('150', 'Commercial Bank'), ('160', 'Investment Bank'), ('170', 'Investment Fund (all types incl. pension, hedge, mutual, private equity funds etc.)'), ('180', 'Insurance firm'), ('190', 'Private equity firm'), ('200', 'Asset management firm'), ('210', 'Non - Profit organization (e.g. Church, University etc.)')], max_length=3),
        ),
    ]

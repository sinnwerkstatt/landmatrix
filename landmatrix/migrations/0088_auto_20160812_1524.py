# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0087_auto_20160710_1744'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='investoractivityinvolvement',
            options={'verbose_name': 'Investor Activity Involvement', 'verbose_name_plural': 'Investor Activity Involvements', 'get_latest_by': 'timestamp', 'ordering': ('-timestamp',)},
        ),
        migrations.AlterModelOptions(
            name='investorventureinvolvement',
            options={'verbose_name': 'Investor Venture Involvement', 'verbose_name_plural': 'Investor Venture Involvements', 'get_latest_by': 'timestamp', 'ordering': ('-timestamp',)},
        ),
        migrations.AlterField(
            model_name='activity',
            name='deal_scope',
            field=models.CharField(verbose_name='Deal scope', db_index=True, choices=[('domestic', 'Domestic'), ('domestic', 'Transnational')], blank=True, null=True, max_length=16),
        ),
        migrations.AlterField(
            model_name='activity',
            name='negotiation_status',
            field=models.CharField(verbose_name='Negotiation status', db_index=True, choices=[('', '---------'), ('Expression of interest', 'Intended (Expression of interest)'), ('Under negotiation', 'Intended (Under negotiation)'), ('Memorandum of understanding', 'Intended (Memorandum of understanding)'), ('Oral agreement', 'Concluded (Oral Agreement)'), ('Contract signed', 'Concluded (Contract signed)'), ('Negotiations failed', 'Failed (Negotiations failed)'), ('Contract cancelled', 'Failed (Contract cancelled)'), ('Contract expired', 'Contract expired'), ('Change of ownership', 'Change of ownership')], blank=True, null=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='filterpreset',
            name='is_default',
            field=models.BooleanField(verbose_name='Country/Region', default=False),
        ),
        migrations.AlterField(
            model_name='filterpreset',
            name='overrides_default',
            field=models.BooleanField(verbose_name='Global', default=False),
        ),
        migrations.AlterField(
            model_name='investorventureinvolvement',
            name='investment_type',
            field=models.CharField(blank=True, null=True, max_length=2, choices=[('10', 'Shares/Equity'), ('20', 'Debt financing')]),
        ),
        migrations.AlterField(
            model_name='investorventureinvolvement',
            name='loans_date',
            field=models.CharField(verbose_name='Loan date', blank=True, null=True, max_length=10),
        ),
    ]

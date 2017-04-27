# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0102_auto_20170424_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='negotiation_status',
            field=models.CharField(null=True, choices=[('', '---------'), ('Expression of interest', 'Intended (Expression of interest)'), ('Under negotiation', 'Intended (Under negotiation)'), ('Memorandum of understanding', 'Intended (Memorandum of understanding)'), ('Oral agreement', 'Concluded (Oral Agreement)'), ('Contract signed', 'Concluded (Contract signed)'), ('Negotiations failed', 'Failed (Negotiations failed)'), ('Contract canceled', 'Failed (Contract cancelled)'), ('Contract expired', 'Contract expired'), ('Change of ownership', 'Change of ownership')], verbose_name='Negotiation status', db_index=True, blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='activitychangeset',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Timestamp'),
        ),
        migrations.AlterField(
            model_name='activityfeedback',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Timestamp'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Timestamp'),
        ),
        migrations.AlterField(
            model_name='historicalactivity',
            name='history_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='historicalinvestor',
            name='history_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='historicalinvestor',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Timestamp'),
        ),
        migrations.AlterField(
            model_name='investor',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Timestamp'),
        ),
        migrations.AlterField(
            model_name='investoractivityinvolvement',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Timestamp'),
        ),
        migrations.AlterField(
            model_name='investorventureinvolvement',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Timestamp'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0067_auto_20160531_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityattributegroup',
            name='polygon',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, srid=4326, null=True),
        ),
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(max_length=10, choices=[('in', 'in'), ('lte', 'lte'), ('contains', 'contains'), ('lt', 'lt'), ('not_in', 'not_in'), ('gt', 'gt'), ('gte', 'gte'), ('is', 'is'), ('is_empty', 'is_empty')], verbose_name='Operator'),
        ),
        migrations.AlterField(
            model_name='historicalactivityattributegroup',
            name='polygon',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, srid=4326, null=True),
        ),
    ]

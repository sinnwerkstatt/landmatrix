# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0045_auto_20160404_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='point_lat_max',
            field=models.DecimalField(max_digits=18, null=True, blank=True, decimal_places=12, verbose_name='Latitude of southernmost point'),
        ),
        migrations.AddField(
            model_name='region',
            name='point_lon_min',
            field=models.DecimalField(max_digits=18, null=True, blank=True, decimal_places=12, verbose_name='Longitude of westernmost point'),
        ),
        migrations.AlterField(
            model_name='country',
            name='point_lat_max',
            field=models.DecimalField(max_digits=18, null=True, blank=True, decimal_places=12, verbose_name='Latitude of southernmost point'),
        ),
        migrations.AlterField(
            model_name='country',
            name='point_lat_min',
            field=models.DecimalField(max_digits=18, null=True, blank=True, decimal_places=12, verbose_name='Latitude of northernmost point'),
        ),
        migrations.AlterField(
            model_name='country',
            name='point_lon_max',
            field=models.DecimalField(max_digits=18, null=True, blank=True, decimal_places=12, verbose_name='Longitude of easternmost point'),
        ),
        migrations.AlterField(
            model_name='country',
            name='point_lon_min',
            field=models.DecimalField(max_digits=18, null=True, blank=True, decimal_places=12, verbose_name='Longitude of westernmost point'),
        ),
        migrations.AlterField(
            model_name='filtercondition',
            name='operator',
            field=models.CharField(max_length=10, choices=[('gte', 'gte'), ('gt', 'gt'), ('not_in', 'not_in'), ('lt', 'lt'), ('in', 'in'), ('is', 'is'), ('contains', 'contains'), ('is_empty', 'is_empty'), ('lte', 'lte')], verbose_name='Operator'),
        ),
        migrations.AlterField(
            model_name='region',
            name='point_lat_min',
            field=models.DecimalField(max_digits=18, null=True, blank=True, decimal_places=12, verbose_name='Latitude of northernmost point'),
        ),
        migrations.AlterField(
            model_name='region',
            name='point_lon_max',
            field=models.DecimalField(max_digits=18, null=True, blank=True, decimal_places=12, verbose_name='Longitude of easternmost point'),
        ),
    ]

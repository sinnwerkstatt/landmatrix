# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landmatrix', '0096_auto_20161109_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='point_lat_max',
            field=models.DecimalField(null=True, max_digits=18, verbose_name='Latitude of northernmost point', blank=True, decimal_places=12),
        ),
        migrations.AlterField(
            model_name='country',
            name='point_lat_min',
            field=models.DecimalField(null=True, max_digits=18, verbose_name='Latitude of southernmost point', blank=True, decimal_places=12),
        ),
    ]
